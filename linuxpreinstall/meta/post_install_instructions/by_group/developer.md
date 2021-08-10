## Manually Install
* bluegriffon: graphical HTML editor [may mangle php]
* zerobrane-studio: Lua editor with the possibility of code completion
* gespeaker
* tsMuxeR
* COLMAP  # (2D to 3D) structure from motion
* GeekBench
* hardinfo  # System Profiler and Benchmark
* renpy [arch community]: Ren'Py is a visual novel engine that helps you use words, images, and sounds to tell interactive stories that run on computers and mobile devices


from source or flatpak for latest version:
  kdenlive
  openshot
  gimp  # if packaged version is not 2.10.8 yet
  #   (~2.10 has wavelet resize and denoise)
from source:
  minetest (see EnlivenMinetest)
  kivy (see above for dependencies)
  lxqt (see $me for packages already installed)

see also Downloads/1.InstallManually
see also ~/Nextcloud/Downloads
and try:
  cd ~/Nextcloud/Downloads/Graphics,2D/gimp-stuff/
  chmod +x install-plugins
  ./install-plugins

To to via GUI"
* Install color profile from
  $HOME/Nextcloud/Downloads/Drivers/Monitor/W2361VV-Windows7/
  or <https://www.lg.com/us/support-product/lg-W2361V-PF>
* Open your linux Desktop's System Settings,
  Color Corrections, Add Profile,
  then choose the downloaded icm profile.
* Enable plugins in Blender:
  - MeasureIT
  - Paint Palettes
    - You must manually set a full path to a palette directory such as:
      - Got to texture paint mode, tools side tab, Color Palette section
      - Paste $HOME/palettes/ (created by $me)
        or other (directory must exist and be writeable) into
        Palettes Folder box.
  - 3D Print Toolbox
  - Extra Objects
  - B3D Exporter (install from file--download github.com/minetest/ fork)
