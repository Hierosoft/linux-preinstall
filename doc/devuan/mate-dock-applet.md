# Dock
(mate-dock-applet)

The MATE Dock applet is a true dock:
- You can hover over an open task then click "Pin ..." to create a permanent shortcut.
- A permanent shortcut becomes a button to switch to the application if the application is running.

For me, my [suggested configuration](../MATE) which includes mate-dock-applet makes MATE as useful as KDE or GNOME but lighter and harder to mess up than an unlocked KDE panel.


## on Devuan 4

I couldn't get it working. Each new panel was invisible. I added several and they got in the way of adding other things but didn't appear.

After several days of system uptime, all of the icons loaded randomly, and I became able to right-click the extra copies of Dock and remove them.

In another case, the following worked:
- Terminate all instances.
- To each MATE panel message asking "Delete", "Don't Reload" or "Reload", choose "Delete".
- Drag Dock to the panel again (In my case, I had added "Window Selector" then added Dock to the right of it).


### Diagnosing

As discussed at [dock applet doesnt appear on panel #7](https://github.com/ubuntu-mate/mate-dock-applet/issues/7) Jun 1, 2015:
- [x] Starting it manually may work (doesn't work for me): `/usr/bin/env python3.9 /usr/lib/mate-applets/mate-dock-applet/dock_applet.py`
- [x] Ensure the dbus service has the correct path to the py file above: `/usr/share/dbus-1/services/org.mate.panel.applet.DockAppletFactory.service`

On Devuan 4 (chimaera) (based on Debian 11 (bullseye)) 2022-08-14:
- Run `sudo apt-get update && sudo apt-get upgrade -y` then restart.
- The py file above says `sys.path.insert(1, '/usr/lib/python3.7/site-packages')` but that directory doesn't exist. In python3 it is dist-packages, and my version is 3.9.
- As discussed at <https://stackoverflow.com/a/46071447/4541104>, you can see the site-packages like: `/usr/bin/env python3 -c 'import site; print(site.getsitepackages())'`
- My result is: `['/usr/local/lib/python3.9/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.9/dist-packages']`
  - /usr/lib/python3.9/dist-packages/ only contains bcrypt
  - /usr/lib/python3/dist-packages/ seems to be the real one
  - /usr/local/lib/python3.9/dist-packages is empty.
- I added the line print("Poikilos: Everything imported") after all of the imports, and it displays when manually running the script.
  - I made a copy called /usr/lib/mate-applets/mate-dock-applet/dock_applet.py.1st
  - I restored the backup.
- The py file says:
  - "Functionality for docked apps is provided in docked_app.py"
  - "Function for the dock is provided in dock.py"
- Based on [paxdiablo's Aug 18, 2010 answer](https://stackoverflow.com/a/3510850/4541104) edited Mar 15, 2017 at 12:38 by Kerem Baydogan at <https://stackoverflow.com/questions/3510673/find-and-kill-a-process-in-one-line-using-bash-and-regex>, terminate a python program via:
  `kill $(ps aux | grep 'dock_app.py' | grep -v grep | awk '{print $2}')`
  - or if you have pkill, based on <https://stackoverflow.com/a/3511301/4541104>:
    `pkill -f dock_app.py`
    - -f: look in full process name
- After going through this a few times I tried dragging Dock instead of adding it, and it worked this time for some reason.
