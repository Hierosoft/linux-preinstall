#!/usr/bin/env python3
from __future__ import print_function

import os
import shutil
import stat
import sys

from collections import OrderedDict
import xml.etree.ElementTree as ET

if sys.version_info.major < 3:
    FileNotFoundError = OSError  # TODO: See if Python 2 has this.
    FileExistsError = OSError  # TODO: See if Python 2 has this.


MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(MODULE_DIR)
sys.path.insert(0, REPO_DIR)

from linuxpreinstall import (
    # compare_versions,
    sorted_versions,
)
# Assemblies known to be not in the Mono GAC
# (and therefore need full path in mcs command)
# - Determined using WineHQ's mono compiled locally
#   2024-09-06 on Linux Mint 22:
EXTERNAL_ASSEMBLIES = [
    "System.Text.Json.dll",
    "System.Threading.dll",
    "System.Reflection.Emit.dll",
    "System.Buffers.dll",
    "System.IO.dll",   # here to avoid version conflicts: See IO_MISMATCH_COMMENT below
    "System.Text.RegularExpressions.dll",
]

# Convert class or namespace from `using` into an actual assembly reference.
REDUNDANT_ASSEMBLIES = {
    "System.Environment": "mscorlib",
    "System.Collections.Generic": "",
    "System.ComponentModel": "System.ComponentModel.Primitives",
    "System.Threading.Tasks": "System.Runtime",
    "System.Runtime.CompilerServices": "System.Runtime",
    "System.Linq": "System.Core",
    "System.Text": "System",  # TODO: or "mscorlib"?
    "System.Media": "System",  # Usage may require System.Windows.Extensions.dll!
    "System.Reflection": "System.Runtime",
    # NOTE: System.Runtime.CompilerServices.Unsafe.dll is only in Mono
    #   4.5 or /usr/local/lib/mono/msbuild/Current/bin/Roslyn/
    # NOTE: System.Text.RegularExpressions is/was a nuget package but
    #   also is in Mono
}

IO_MISMATCH_COMMENT = """
Unhandled Exception:
System.NotImplementedException: The method or operation is not implemented.
  at System.IO.Ports.SerialPort.set_DiscardNull (System.Boolean value) [0x00000] in <b95dfe79e58c4102b7a41d3edfa6bb32>:0 
  at (wrapper remoting-invoke-with-check) System.IO.Ports.SerialPort.set_DiscardNull(bool)
  at {namespace}.MainForm.InitializeComponent () [0x0023d] in <9300349e8d174f3fa3783e7ccae42068>:0 
  at {namespace}.MainForm..ctor () [0x00056] in <9300349e8d174f3fa3783e7ccae42068>:0 
  at (wrapper remoting-invoke-with-check) {namespace}.MainForm..ctor()
  at {namespace}.Program.Main () [0x0000b] in <9300349e8d174f3fa3783e7ccae42068>:0 
[ERROR] FATAL UNHANDLED EXCEPTION: System.NotImplementedException: The method or operation is not implemented.
  at System.IO.Ports.SerialPort.set_DiscardNull (System.Boolean value) [0x00000] in <b95dfe79e58c4102b7a41d3edfa6bb32>:0 
  at (wrapper remoting-invoke-with-check) System.IO.Ports.SerialPort.set_DiscardNull(bool)
  at {namespace}.MainForm.InitializeComponent () [0x0023d] in <9300349e8d174f3fa3783e7ccae42068>:0 
  at {namespace}.MainForm..ctor () [0x00056] in <9300349e8d174f3fa3783e7ccae42068>:0 
  at (wrapper remoting-invoke-with-check) {namespace}.MainForm..ctor()
  at {namespace}.Program.Main () [0x0000b] in <9300349e8d174f3fa3783e7ccae42068>:0
"""

IMPLIED_ASSEMBLIES = {
    "System.Text.Json.dll": ["System.Buffers.dll"],
    # avoid: "System.TypeInitializationException: The type initializer for '{namespace}.MainForm' threw an exception. ---> System.IO.FileNotFoundException: Could not load file or assembly 'System.Buffers, Version=4.0.2.0, Culture=neutral, PublicKeyToken=cc7b13ffcd2ddd51' or one of its dependencies.
    #  at System.Text.Json.JsonDocument.Parse (System.String json, System.Text.Json.JsonDocumentOptions options) [0x00014] in <83434c3504484469bfe9fa2ebdb16a14>:0"
}

# Only needs to be one value since if more you can use the value as a key in
#   IMPLIED_ASSEMBLIES (add dependency there instead).
# USING_ASSEMBLIES = {
#     "System.IO": "System.IO.dll",
# }

# Mono reference assembly directories
#   (for finding assemblies not in the GAC)
ASSEMBLY_DIRS = OrderedDict()
ASSEMBLY_DIRS["FACADES_DIR"] = "/opt/git/mono/external/binary-reference-assemblies/v4.8/Facades"
ASSEMBLY_DIRS["MSBUILD_BIN_DIR"] = "/usr/lib/mono/msbuild/Current/bin"

LOCAL_LIB_MONO = "/usr/local/lib/mono/"
LOCAL_LIB_MONO_VERSIONS = []
for sub in os.listdir(LOCAL_LIB_MONO):
    sub_path = os.path.join(LOCAL_LIB_MONO, sub)
    if sub.startswith("."):
        continue
    if not os.path.isdir(sub_path):
        continue
    # if not sub[:1].isdigit():
    #     # This should be handled by sort_versions instead, version -1
    #     # Actually, also prevented by it not having a Facades dir below
    #     continue
    if not os.path.isdir(os.path.join(sub_path, "Facades")):
        # No Facades dir, so no assemblies
        continue
    LOCAL_LIB_MONO_VERSIONS.append(sub)

if LOCAL_LIB_MONO_VERSIONS:
    for sub in reversed(sorted_versions(LOCAL_LIB_MONO_VERSIONS, quiet=True)):
        # ^ quiet=True to ignore (they will be considered version < 0)
        # TODO: See if -api dir is better or worse (example: "4.8-api")
        sub_path = os.path.join(LOCAL_LIB_MONO, sub, "Facades")
        print("Using \"%s\" instead of \"%s\""
              % (sub_path, ASSEMBLY_DIRS["FACADES_DIR"]))
        ASSEMBLY_DIRS["FACADES_DIR"] = sub_path
        break

USED_BASH_VARS = []


def find_assembly(relative_path, with_bash_var=False):
    """Find the assembly in the specified directories.

    Args:
        relative_path (str): The relative path of the assembly--
            relative to the GAC, so usually a .NET reference assembly
            (dll) filename only.
        with_bash_var (optional, bool): If the file is found,
            return a bash variable combined with relative_path
            representing the full path. If False return a full path.
            Defaults to False.

    Returns:
        str or None: The absolute path if found, otherwise None.
    """
    for key, parent in ASSEMBLY_DIRS.items():
        try_path = os.path.join(parent, relative_path)
        if os.path.exists(try_path):
            if with_bash_var:
                USED_BASH_VARS.append(key)
                return "$%s/%s" % (key, relative_path)
            return try_path
        print("No '%s'" % try_path)
    return None


class CSProject:
    """Handle CSProject file processing and shell script generation.

    Attributes:
        cs_files (list of str): A list of C# source file paths collected from
            the .csproj file.
        assemblies (list of str): A list of assembly references collected from
            the .csproj file.
        out_dir (str): The output directory where the compiled binaries will
            be placed. Extracted from the OutputPath element in the .csproj file
            and stripped of trailing slashes.
        out_name (str): The name of the output executable. Obtained from the
            AssemblyName from the .csproj file with a ".exe" extension. If not
            available, defaults to the base name of the .csproj file with a
            ".exe" extension.
        top_comments (list of str): A list of comments to be included at the
            top of the generated bash script. Loaded from "project.comments.top.txt"
            if the file exists.
        build_comments (list of str): A list of comments to be included in the
            build section of the generated bash script. Loaded from
            "project.comments.build.txt" if the file exists.
        meta (OrderedDict): A nested ordered dictionary for storing additional
            metadata from the .csproj file. Can be extended to include more
            details as needed.
    """

    def __init__(self):
        self.cs_files = []
        self.assemblies = []
        self.out_dir = 'bin'
        self.out_name = None
        self.top_comments = []
        self.build_comments = []
        self.meta = OrderedDict()

    def load(self, source):
        """Load the project file and extract necessary information.

        Args:
            source (str): The path to the .csproj file.
        """
        other_os_sep = "\\" if (os.path.sep == "/") else "/"
        tree = ET.parse(source)
        root = tree.getroot()
        namespace = '{http://schemas.microsoft.com/developer/msbuild/2003}'

        # Extract AssemblyName from PropertyGroup
        assembly_name_element = root.find(
            "%sPropertyGroup/%sAssemblyName" % (namespace, namespace)
        )
        if assembly_name_element is not None:
            self.out_name = "%s.exe" % assembly_name_element.text
        else:
            self.out_name = "%s.exe" % os.path.splitext(source)[0]

        # Extract OutputPath from PropertyGroup
        output_path_element = root.find(
            "%sPropertyGroup/%sOutputPath" % (namespace, namespace)
        )
        if output_path_element is not None:
            self.out_dir = output_path_element.text.rstrip("\\/")
            self.out_dir = \
                self.out_dir.replace(other_os_sep, os.path.sep)
            if self.out_dir.startswith("/bin") or (self.out_dir == "/"):
                # for safety:
                self.out_dir = self.out_dir.lstrip("\\/")
                # ^ '' is ok since os.path.join('', no_leading_slash)
                #   results in a relative path.

        # Collect assembly references
        self.assemblies = [
            ref.get('Include') for ref in root.findall(
                "%sItemGroup/%sReference" % (namespace, namespace)
            )
        ]

        source_dir = os.path.dirname(source)
        # Collect source files first so implied references can be collected.
        self.cs_files = [
            file.get('Include') for file in root.findall(
                "%sItemGroup/%sCompile" % (namespace, namespace)
            )
        ]
        # self.load_comments()
        more_assemblies = OrderedDict()
        using_keyword = b"using"
        for i in range(len(self.cs_files)):
            self.cs_files[i] = \
                self.cs_files[i].replace(other_os_sep, os.path.sep)
            cs_path = os.path.join(source_dir, self.cs_files[i])
            if not os.path.isfile(cs_path):
                print(
                    "Error: Missing \"%s\" so \"using\" statements"
                    " will not be validated." % cs_path)
                continue
            with open(cs_path, "rb") as stream:
                for line in stream:
                    if line.startswith(b"#"):
                        continue
                    if line.strip().startswith(b"namespace"):
                        # The using statements better be over.
                        break
                    if line.strip().startswith(b"class"):
                        # The using statements better be over.
                        break
                    using_i = line.find(using_keyword)
                    if using_i < 0:
                        continue
                    start = using_i + len(using_keyword)
                    end = line.find(b";", start)
                    if end != -1:
                        result = line[start:end].strip().decode("utf-8")
                        parts = result.split()
                        if len(parts) > 1:
                            print("INFO: ignored \"%s\" in \"using %s\""
                                  % (" ".join(parts[:-1]), result))
                            result = parts[-1]
                        redundant_assembly = REDUNDANT_ASSEMBLIES.get(result)
                        if redundant_assembly:
                            if redundant_assembly not in more_assemblies:
                                print("Using assembly %s for redundant %s"
                                    % (redundant_assembly, result))
                            result = redundant_assembly
                            # Example: Change System.Environment to System
                            #   (System.Environment is not an assembly, it is a
                            #   namespace in the System assembly)
                        else:
                            if result not in more_assemblies:
                                print("Using non-redundant assembly %s" % result)
                        # ^ Fix strings such as `using static System.Environment;`
                        if result not in more_assemblies:
                            more_assemblies[result] = []
                        more_assemblies[result].append(self.cs_files[i])
                        # ^ Use as key so it is only added once below.
        for assembly, cs_files in more_assemblies.items():
            assembly_file = assembly + ".dll"
            if ((assembly not in self.assemblies)
                    and (assembly_file not in self.assemblies)):
                print("Warning: A reference to %s will be"
                      " automatically added since used in %s"
                      % (assembly, cs_files))
                self.assemblies.append(assembly)
        for using_name, assembly in REDUNDANT_ASSEMBLIES.items():
            using_file_bad = using_name + ".dll"
            if using_file_bad in self.assemblies:
                raise ValueError("Non-existent assembly %s should be %s"
                                 % (using_file_bad, assembly))
        # NOTE: Any IMPLIED_ASSEMBLIES are added in the emit_bash method.
        for i in range(len(self.assemblies)):
            self.assemblies[i] = \
                self.assemblies[i].replace(other_os_sep, os.path.sep)
            if not self.assemblies[i].lower().endswith(".dll"):
                endI = self.assemblies[i].find(", ")
                if endI >= 0:
                    # such as in "System.Memory, Version=4.0.1.1,
                    # Culture=neutral, PublicKeyToken=cc7b13ffcd2ddd51,
                    # processorArchitecture=MSIL.dll"
                    self.assemblies[i] = self.assemblies[i][:endI]
                self.assemblies[i] = self.assemblies[i].replace("\\", os.path.sep)
                self.assemblies[i] += ".dll"


        self.meta = OrderedDict()  # reserved for future use (get more metadata)

    def load_comments(self):
        # Load comments if files exist
        if os.path.isfile("project.comments.top.txt"):
            with open("project.comments.top.txt") as f:
                self.top_comments = f.readlines()
        if os.path.isfile("project.comments.build.txt"):
            with open("project.comments.build.txt") as f:
                self.build_comments = f.readlines()

    def write_as_comments(self, f, lines):
        if lines:
            for rawL in lines:
                line = rawL.rstrip()
                if not line.lstrip().startswith("#") and line.strip():
                    line = "# " + line
                f.write("%s\n" % line)

    def emit_bash(self, path, force=False):
        """Emit a bash script based on the loaded project data.

        Args:
            path (str): The path where the bash script will be written.
            force (bool): Overwrite the destination if it exists.
        """
        print("Writing %s..." % path)
        results = {'warnings': []}
        if os.path.isfile(path) and not force:
            raise FileExistsError("File \"%s\" already exists."
                                  % os.path.abspath(path))

        self.load_comments()
        tmp_path = path + ".tmp"  # use tmp to prevent corrupt output if fails
        MCS = "mcs"
        for try_mcs in ["/usr/local/bin/mcs"]:
            # To get /usr/local/bin/mcs, see
            #   mono-from-source.*.sh
            if os.path.isfile(try_mcs):
                MCS = try_mcs
                break
        with open(tmp_path, "w") as f:
            f.write("#!/bin/bash\n")
            self.write_as_comments(f, self.top_comments)

            # Write environment variables
            for key, value in ASSEMBLY_DIRS.items():
                f.write("%s=%s\n" % (key, value))
            f.write("OUTPUT_DIR=%s\n\n" % self.out_dir)
            f.write("mkdir -p \"$OUTPUT_DIR\"\n")

            # Construct the mcs command
            references = OrderedDict()
            dll_paths = OrderedDict()
            for assembly in self.assemblies:
                implied_assemblies = IMPLIED_ASSEMBLIES.get(assembly)
                if implied_assemblies:
                    for implied_assembly in implied_assemblies:
                        if implied_assembly not in self.assemblies:
                            self.assemblies.append(implied_assembly)
            for assembly in self.assemblies:
                minimum_path = assembly
                if minimum_path in EXTERNAL_ASSEMBLIES:
                    minimum_path = find_assembly(assembly, with_bash_var=True)
                    if not minimum_path:
                        raise FileNotFoundError("%s not found." % assembly)
                dll_paths[assembly] = find_assembly(assembly)
                references[assembly] = minimum_path

            f.write("echo \"compiling '%s/%s'\"\n"
                    % (self.out_dir, self.out_name))
            f.write("%s -out:\"%s/%s\" \\\n"
                    % (MCS, self.out_dir, self.out_name))
            for _, reference in references.items():
                f.write('    -r:%s \\\n' % reference)

            for cs_file in self.cs_files:
                f.write("    \"%s\" \\\n" % cs_file)
            f.write("    1>out.txt 2>err.txt\n")
            f.write("code=$?\n\n")

            self.write_as_comments(f, self.build_comments)

            # Copy referenced DLLs
            for rel_path, abs_path in dll_paths.items():
                if abs_path:
                    f.write('cp "%s" "$OUTPUT_DIR/"\n' % abs_path)
                else:
                    error = ('MISSING assembly "%s",'
                             ' can\'t copy to "$OUTPUT_DIR"'
                             % rel_path)
                    results['warnings'].append(error)
                    print("Error: %s" % error, file=sys.stderr)
                    # ^ Error: MISSING assembly
                    f.write('# %s\n' % error)

            # Handle output inspector
            f.write("\ncode=$?\n")
            f.write("if [ -f \"$(command -v outputinspector)\" ]; then\n")
            f.write("    if [ $code -ne 0 ]; then\n")
            f.write("        echo \"FAILED\"\n")
            f.write("    else\n")
            f.write("        echo \"SUCCESS\"\n")
            f.write("    fi\n")
            f.write("    killall outputinspector\n")
            f.write("    outputinspector&\n")
            f.write("else\n")
            f.write("    cat out.txt\n")
            f.write("    cat err.txt\n")
            f.write("    if [ $code -ne 0 ]; then\n")
            f.write("        echo \"FAILED\"\n")
            f.write("    else\n")
            f.write("        echo \"SUCCESS\"\n")
            f.write("    fi\n")
            f.write("fi\n")
            f.write("\n# Exit with the same code as the compilation command\n")
            f.write("exit $code\n")
        if os.path.isfile(path) and force:
            os.remove(path)
        shutil.move(tmp_path, path)
        print("Wrote \"%s\"" % path)
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        # S_IXUSR, S_IXGRP, S_IXOTH: executable for owner, group, other,
        #   respectively
        return results


def csproj_to_build_sh(source, destination, force=False):
    """Convert a .csproj file to a bash build script.

    Args:
        source (str): The path to the .csproj file.
        dest (str): The path to the output bash script.
    """
    project = CSProject()
    project.load(source)
    project.emit_bash(destination, force=force)


def main():
    if len(sys.argv) < 2:
        print("Error: you must specify a csproj filename in the current directory.")
        return 1
    csproj_path = sys.argv[1]
    _, name = os.path.split(csproj_path)
    if not os.path.isfile(name):
        print("Error: you must specify a csproj filename in the current directory.")
        return 1
    destination = "build-%s.sh" % os.path.splitext(name)[0]
    force = False
    if "--force" in sys.argv:
        force = True
    csproj_to_build_sh(name, destination, force=force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
