#!/usr/bin/env python3
from __future__ import print_function

import os
import shutil
import sys

from collections import OrderedDict
import xml.etree.ElementTree as ET

if sys.version_info.major < 3:
    FileNotFoundError = OSError  # TODO: See if Python 2 has this.
    FileExistsError = OSError  # TODO: See if Python 2 has this.

# Assemblies known to be not in the Mono GAC
# (and therefore need full path in mcs command)
# - Determined using WineHQ's mono compiled locally
#   2024-09-06 on Linux Mint 22:
EXTERNAL_ASSEMBLIES = [
    "System.Text.Json.dll",
    "System.Threading.dll",
    "System.Reflection.Emit.dll"
]

# Mono reference assembly directories
#   (for finding assemblies not in the GAC)
ASSEMBLY_DIRS = {
    "MSBUILD_BIN_DIR": "/usr/lib/mono/msbuild/Current/bin",
    "FACADES_DIR": "/opt/git/mono/external/binary-reference-assemblies/v4.8/Facades"
}

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
        for i in range(len(self.assemblies)):
            if not self.assemblies[i].lower().endswith(".dll"):
                endI = self.assemblies[i].find(", ")
                if endI >= 0:
                    # such as in "System.Memory, Version=4.0.1.1,
                    # Culture=neutral, PublicKeyToken=cc7b13ffcd2ddd51,
                    # processorArchitecture=MSIL.dll"
                    self.assemblies[i] = self.assemblies[i][:endI]
                self.assemblies[i] = self.assemblies[i].replace("\\", os.path.sep)
                self.assemblies[i] += ".dll"

        # Collect source files
        self.cs_files = [
            file.get('Include') for file in root.findall(
                "%sItemGroup/%sCompile" % (namespace, namespace)
            )
        ]
        # self.load_comments()
        for i in range(len(self.cs_files)):
            self.cs_files[i] = self.cs_files[i].replace("\\", os.path.sep)

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

    def emit_bash(self, path):
        """Emit a bash script based on the loaded project data.

        Args:
            path (str): The path where the bash script will be written.
        """
        print("Writing %s..." % path)
        results = {'warnings': []}
        if os.path.isfile(path):
            raise FileExistsError("File \"%s\" already exists." % os.path.abspath(path))

        self.load_comments()
        tmp_path = path + ".tmp"  # use tmp to prevent corrupt output if fails
        with open(tmp_path, "w") as f:
            f.write("#!/bin/bash\n")
            self.write_as_comments(f, self.top_comments)

            # Write environment variables
            for key, value in ASSEMBLY_DIRS.items():
                f.write("%s=%s\n" % (key, value))
            f.write("OUTPUT_DIR=%s\n\n" % self.out_dir)

            # Construct the mcs command
            references = OrderedDict()
            dll_paths = OrderedDict()
            for assembly in self.assemblies:
                minimum_path = assembly
                if minimum_path in EXTERNAL_ASSEMBLIES:
                    minimum_path = find_assembly(assembly, with_bash_var=True)
                dll_paths[assembly] = find_assembly(assembly)
                references[assembly] = minimum_path

            f.write("mcs -out=\"%s/%s\" \\\n" % (self.out_dir, self.out_name))
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
                    error = 'MISSING "%s", can\'t copy to "$OUTPUT_DIR"' % rel_path
                    results['warnings'].append(error)
                    print("Error: %s" % error, file=sys.stderr)
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
        shutil.move(tmp_path, path)
        print("Wrote \"%s\"" % path)
        return results


def csproj_to_build_sh(source, destination):
    """Convert a .csproj file to a bash build script.

    Args:
        source (str): The path to the .csproj file.
        dest (str): The path to the output bash script.
    """
    project = CSProject()
    project.load(source)
    project.emit_bash(destination)


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
    csproj_to_build_sh(name, destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
