# Corrected Geany Configuration for OpenSCAD Editing (+ shell script installer)
<https://www.thingiverse.com/thing:5327783>
(based on [Geany Configuration for OpenSCAD Editing](https://www.thingiverse.com/thing:263620) by [cobra18t](https://www.thingiverse.com/cobra18t) March 05, 2014)

## Differences in Poikilos remix
- Store settings in AppData (or ~/.config) so that the system-wide configuration remains intact and the new configuration isn't undone when Geany is updated.
- The number of lines is reduced so that unrelated system-wide defaults are not overwritten (as per a comment on the original thing).
- The correct subdirectory "filedefs" is used under the geany application data so that the installation works (as per a comment on the original thing).

## Features
- Auto-Completion
- Syntax Highlighting
- Collapsible Outline levels
- Line Numbering
- Automatic Tabbing
- Parenthesis/Bracket Completion
- Search and Replace
- Block Tabbing using the tab key

## Requires
- Geany
- OpenSCAD (only to preview/render your scad files)

## Install

### Get the files (alternate steps)
Right-click each file listed below, then right-click then "Save link as" or any similar save feature depending on your browser (If using the repo left-click the filename then right-click "Raw" then save). The files geany-openSCAD.sh and the configuration file are maintained in the "developer" folder at <https://github.com/poikilos/linux-preinstall> (See `geany-openscad.*`).
- Download [geany-openSCAD.sh](https://github.com/poikilos/linux-preinstall/raw/master/developer/geany-openscad.sh) (not required for the "Install on Windows" steps).
- Download [uploads_42_3c_3d_83_43_filetypes.OpenSCAD.conf](https://github.com/poikilos/linux-preinstall/raw/master/developer/uploads_42_3c_3d_83_43_filetypes.OpenSCAD.conf) to the same folder.

### Get the files
- uploads_42_3c_3d_83_43_filetypes.OpenSCAD.conf
- geany-openSCAD.sh (not required for the "Install on Windows" steps)

(ignore the dummy file--it is there because Thingiverse requires a model file. Otherwise it says, "A Thing must have at least one file of type: stl, obj, thing, scad, amf, dae, 3ds, x3d, blend, ply, dxf, ai, svg, cdr, ps, eps, epsi, sch, brd")


### Install on GNU+Linux systems
- Complete the steps under "Get the Files" above.
- Open a Terminal
- `cd` to the directory (such as via `cd ~/Downloads`)
- Run `bash geany-openSCAD.sh`.

### Install on Windows
- Complete the steps under "Get the Files" above.
- Right-click start, click Run
- Paste "%APPDATA%\geany" then press enter (If it has an error, install and run Geany then close it then try this step again).
- If there is no "filedefs" folder, create it using the small New Folder button.
- Save the included uploads_42_3c_3d_83_43_filetypes.OpenSCAD.conf file to
- Open Geany
- Click "Tools", "Configuration files", "filetype_extensions.conf"
- Paste the following:

```
[Extensions]
OpenSCAD=*.scad;
#Editing groups requires restarting Geany
[Groups]
Script=OpenSCAD
```

- Save the file.
- Exit Geany & reopen it.
- Close & reopen any scad files you had open (The file type "None" would still be set unless opened after the new file type was installed).


## Use
- Arrange both OpenSCAD and Geany on your screen/s so that both can be seen at once.
- Open your scad file in both editors.
- Edit your .scad file in Geany. Each time you save the file (Ctrl+s) you will see that OpenSCAD will recompile the object. With the updated filename\_extensions.conf file, .scad files should be automatically recognized and the syntax will be highlighted appropriately. You can get other color themes for Geany.

## License
Copyright (c) 2014 cobra18t, 2022 Poikilos
[Creative Commons Attribution-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/) (CC BY-SA 3.0)

## Summary
[by cobra18t]

I wanted a more powerful editor for OpenSCAD scripts that was natively cross platform (i.e. no WINE use). After seeing Justblair's thing:15363, I decided to get something working on my text editor of choice, Geany.

Check the instructions...

This gives you:
Auto-Completion
Syntax Highlighting
Collapsible Outline levels
Line Numbering
Automatic Tabbing
Parenthesis/Bracket Completion
Search and Replace
Block Tabbing using the tab key.

Instructions

I assume you already have OpenSCAD and Geany

1. Copy filetypes.OpenSCAD.conf to the Geany directory with all the other filetype files.
  - Ubuntu: /usr/share/geany
  - Windows: `C:\Program Files\Geany\data`

2. Copy filetype\_extensions.conf to the same folder replacing the one there or edit the one there with the two lines shown in the fourth attached image.

3. Open OpenSCAD, Create a new file and save it.

4. In the Design menu select Automatic Reload and Compile

5. In the View menu select Hide editor

6. Leaving OpenSCAD running, now find your newly created .scad file in a file explorer, right hand click on it and select Open with Geany

7. Visit the Edit > Preferences menu in Geany and change the preferences for auto completion, indentation, and display as shown in attached images 5-7.

8. Arrange both OpenSCAD and Geany on your screen/s so that both can be seen at once.

9. Edit your .scad file in Geany. Each time you save the file (CTRL+S) you will see that OpenSCAD will recompile the object. With the updated filename\_extensions.conf file, .scad files should be automatically recognized and the syntax will be highlighted appropriately. You can get other color themes for Geany.

10. Enjoy all the advanced text editing features of Geany as well as syntax highlighting of your code!!!

## Tags
Code syntax syntax_highlight openscad_editor text-editor text_editor openscad script openscad_script
