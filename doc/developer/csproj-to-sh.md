# csproj to sh

## Planning
Make a python py script that automatically reads the project file using the xml module, then constructs a shell script like that and runs it. The py script should have a list called external_assemblies that contains System.Text.Json.dll, System.Threading.dll, and System.Reflection.Emit.dll. The py file should have a dict assembly_dirs = {"MSBUILD_BIN_DIR": "/usr/lib/mono/msbuild/Current/bin", "FACADES_DIR": "/opt/git/mono/external/binary-reference-assemblies/v4.8/Facades". Make a global function called find_assembly that accepts a relative_path, iterates for parent in assembly_dirs, try_path = os.path.join(parent, relative_path), if os.path.exists(try_path) return try_path. After the loop, return None. The main function should call csproj_to_build_sh(sys.argv[1], "build.sh") and return 0. if __name__ == "__main__": sys.exit(main()). csproj_to_build_sh should be the function with  source and destination arguments. It should instantiate a class as project = CSProject(), then call project.load(). The load method reads the source using the xml module, collects all of the dependencies into a list, and collects any other data you may need. It checks to see if there is a file called "project.comments.top.txt" and if so, reads the lines into a list called self.top_comments. If there is a file called "project.comments.build.txt" it loads it into a list called self.build_comments. The relative cs file paths should go in a list called self.cs_files, the assemblies should go in a list called self.assemblies, and the output dir should be stored as out_dir and the output assembly name should be stored as self.out_name. Save any other info from the project files similar to one I gave you that may be helpful later, using dicts and lists in whatever way fits best, nested ones being ok. preferably save any data I didn't mention above to a nested self.meta OrderedDict with any list children being list, and and dict children being OrderedDict. The class should have a emit_bash method as well, that accepts a path argument. The method should raise IOError if os.path.isfile(path); then iterate assembly_dirs to write the "%s=%s" % (key, value) lines. also write the "OUTPUT_DIR=%s" % self.out_dir line. then set cs_paths = OrderedDict() and iterate for cs_file in cs_files, set cs_path = find_assembly(cs_file), add result to cs_paths[cs_file, cs_path]; open path  in "w" mode, write  bash shebang, write self.top_comments if any, construct the mcs command in the multi-line format I provided using "mcs -out" + os.path.join(self.out_dir, self.out_name) + "\\" as the first line, iterate self.cs_files to create the '    "{cs_file}" \\' lines, create the "    1>out.txt 2>err.txt" line, "code=$?" line, blank line, & write self.build_comments if any, each stripped then indented 4 spaces. Don't put any of the large comment blocks in, just ones I am describing in the order I'm describing. Next iterate for rel_path, abs_path in cs_path in cs_paths.items() and construct the "cp %s $OUTPUT_DIR" % abs_path lines. Next put the outputinspector handling code, the "# Exit with the same code as the compilation command" comment line, the "exit $code" line. For backward compatibility use percent sign notation for any substitutions, as well as start the script with a python shebang and from __future__ import print_function. Follow PEP8, especially trying to limit comments to 72 characters and code to 79 characters, using parenthesis and string continuation if necessary to avoid mangling strings. Document everything with Google-style docstrings.