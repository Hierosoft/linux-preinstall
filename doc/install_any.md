# install_any
Install **any** software (including deb) using ONE COMMAND on **any** GNU-like OS!

Step 1: install_any.py <packagename>
- There is only one step!
- It installs in user space (~/.local, so add ~/.local/bin to your path--see the "Install" section).
- It keeps uninstall metadata in ~/.config/install_any/

Install an archive (deb, zip, gz, bz2), binary (including appimage) or directory onto ANY GNU-like OS!
- A shortcut will **always** be created automatically.
- If there is a subdirectory in the archive, that will be detected and handled properly!
- If it is a binary (including appimage), that will be detected and handled properly!
- If there is no icon, and the icon is in `iconLinks`, that will be downloaded and used!

This software was formerly a script in https://github.com/poikilos/linux-preinstall/utilities.


## Author and license
Author: Jake "Poikilos" Gustafson
License: See license.txt


## Internet use
This script will try to download the icon if an icon isn't known to be
included but is known to be online. You can see the list of possible
URLs that will be accessed by viewing the iconLinks dictionary in
install_any.py


## Install
```
mkdir -p ~/git
cd ~/git
git clone https://github.com/poikilos/linux-preinstall.git ~/git/linux-preinstall
cd linux-preinstall/utilities
./install_ia-nonroot.sh
```


## Metadata
The metadata for each installed or uninstalled program is stored
permanently in local_machine.json located at
~/.config/install_any/local_machine.json. If you delete it, the next
run will try to regenerate it from
~/.config/install_any/install_any.log (which doesn't preserve
multi-version data, so the generated metadata will only refer to the
last version installed using install_any) unless you delete that too.
The install or uninstall process will try to derive the version,
shortcut caption string, unique program name (called "luid" in the
code), and package name from the filename or directory name provided,
unless you specify such strings manually (they will be passed on to the
install_program_in_place function then to PackageInfo init).

### luid
The luid is a "locally-unique ID" that represents the program. If
multiVersion is enabled, see the "sc_name" section.

#### Uninstalling or installing using luid
If you know the luid (locally-unique ID) of a program and it is in the
programs object in local_machine.json, you can uninstall the program
using the luid (otherwise you need the full path of the source, which
may be inaccessible). You can obtain the luid of any installed program
by reviewing local_machine.json after the first run of the program. For
examples, see the docstring of the main py file.

### Multi-version support
You can enable multiVersion to install multiple copies of a program
with different versions. It will be enabled automatically if the
program is usually multiversion when installed manually, such as
blender (If you're installing blender manually for some other reason,
there is no penalty--multiVersion simply makes a separate shortcut icon
that says the version in the caption after the name of the program).

#### sc_name
The `sc_name` is the package named (named `sc_name` since it is also the
shortcut filename--See 'packages' in local_machine.json, which will
only be populated in cases where multiVersion is enabled). The package
name will uniquely identify the program in case multiVersion is
enabled, but the luid will also remain as a way to track the package
back to a unique program (in 'programs' in local_machine.json). If
multiVersion is not enabled, `sc_name` will be.
