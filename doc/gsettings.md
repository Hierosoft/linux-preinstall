# gsettings

## Reload settings
`mate-panel --replace &`

Full reload, including closing applications:
```
#!/bin/bash
mate-settings-daemon --replace &
mate-panel --replace &
marco --no-composite --replace &
killall mate-volume-control-applet
killall caja
mate-volume-control-applet &
killall compton
compton &
```

-by Jesus_Eguiluz on [How to restart/refresh MATE without logout?](https://ubuntu-mate.community/t/how-to-restart-refresh-mate-without-logout/13726/16)

## MATE
### Brisk Menu

The linux-preinstall command `sort-mate-brisk-menu-favs` can sort the
favorites ("Favourites" (en_GB)) menu.

Menu settings and brisk-menu settings are stored in dconf and accessed via the gsettings command
(See <https://askubuntu.com/questions/805144/how-do-i-restore-mate-panel-settings-from-old-backup>).

- `gsettings list-schemas | grep brisk` yields: com.solus-project.brisk-menu
- `gsettings list-keys com.solus-project.brisk-menu`:
  - label-visible
  - pinned-shortcuts
  - favourites
  - rollover-activate
  - dark-theme
  - hot-key
  - label-text
  - search-position
  - window-type
- `gsettings get com.solus-project.brisk-menu favourites` yields:
  - `['world_clock.desktop', 'org.minetest.minetest-logged.desktop', 'thunar.desktop', 'caja-browser.desktop', 'mate-appearance-properties.desktop', 'thunderbird.desktop', 'xfce4-terminal.desktop', 'appimagekit_1f378f83322537003449bd70bfb60a2e-Telegram_Desktop.desktop', 'org.strawberrymusicplayer.strawberry.desktop', 'speedcrunch.desktop', 'spacefm.desktop', 'mate-disk-usage-analyzer.desktop', 'com.prusa3d.PrusaSlicer.desktop', 'prusaslicer-AppImage.desktop', 'libreoffice-startcenter.desktop', 'keepassxc-AppImage.desktop', 'org.kde.kdenlive.desktop', 'net.scribus.Scribus.desktop', 'org.inkscape.Inkscape.desktop', 'org.gimp.GIMP.desktop', 'zbstudio.desktop', 'godot-3.3.2-stable.desktop', 'samurai-ide.desktop', 'geany.desktop', 'org.mozilla.firefox.desktop', 'ultimaker.cura-AppImage.desktop', 'blender-3.0.1.desktop', 'blender-2.92.0.desktop', '4kvideodownloader.desktop', 'spyder.desktop', 'org.minetest.minetest-220509-logged.desktop']`
- sort via:
  - gsettings set com.solus-project.brisk-menu favourites "['world_clock.desktop', 'org.minetest.minetest-logged.desktop', 'org.minetest.minetest-220509-logged.desktop', 'thunar.desktop', 'caja-browser.desktop', 'mate-appearance-properties.desktop', 'thunderbird.desktop', 'xfce4-terminal.desktop', 'appimagekit_1f378f83322537003449bd70bfb60a2e-Telegram_Desktop.desktop', 'org.strawberrymusicplayer.strawberry.desktop', 'speedcrunch.desktop', 'spacefm.desktop', 'mate-disk-usage-analyzer.desktop', 'com.prusa3d.PrusaSlicer.desktop', 'prusaslicer-AppImage.desktop', 'libreoffice-startcenter.desktop', 'keepassxc-AppImage.desktop', 'org.kde.kdenlive.desktop', 'net.scribus.Scribus.desktop', 'org.inkscape.Inkscape.desktop', 'org.gimp.GIMP.desktop', 'zbstudio.desktop', 'godot-3.3.2-stable.desktop', 'samurai-ide.desktop', 'geany.desktop', 'org.mozilla.firefox.desktop', 'ultimaker.cura-AppImage.desktop', 'blender-3.0.1.desktop', 'blender-2.92.0.desktop', '4kvideodownloader.desktop', 'spyder.desktop']"
  - "The value is specified as a serialised GVariant" -<https://manpages.ubuntu.com/manpages/trusty/man1/gsettings.1.html>
  - `mate-settings-daemon --replace &` (may not be necessary--seems to reload panel but "favourites" order isn't updated.
  - `mate-panel --replace &`
