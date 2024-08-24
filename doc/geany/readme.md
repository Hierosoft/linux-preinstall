# linux-preinstall Geany components

## Epsilon Dark Theme
The files are located at https://github.com/Hierosoft/linux-preinstall/tree/master/AlwaysAdd/HOME/.config/geany

Installation:
```
git clone https://github.com/Hierosoft/linux-preinstall.git linux-preinstall
cd linux-preinstall && mkdir -p ~/.config/geany/colorschemes && cp ./AlwaysAdd/HOME/.config/geany/colorschemes/epsilon-dark.conf ~/.config/geany/colorschemes/
```

Then go to Geany, "View", "Change Color Scheme..." and choose "Epsilon Dark".

Only the code window will change. To make the rest of Geany dark, change your desktop theme using your themes application. This will affect all applications that correctly utilize desktop theme colors.
