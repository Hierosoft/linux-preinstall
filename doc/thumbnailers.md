# Thumbnailers

A thumbnailer lets you see a preview of the files in a list. If you cannot see previews of certain file types, there may be a thumbnailer you can install to resolve the issue.


## STL/OBJ thumbnails
(As discussed at <https://www.reddit.com/r/3Dprinting/comments/rbh7wj/linux_enabling_stlobj_thumbnails_in_linux/>)
- [f3d releases](https://github.com/f3d-app/f3d/releases)
  but it has a bad angle (top view). So add `--camera-azimuth-angle=0 --camera-elevation-angle=-45` to:
  - /usr/share/thumbnailers/f3d-plugin-native.thumbnailer
  - /usr/share/thumbnailers/f3d-plugin-assimp.thumbnailer
  - clear ~/.cache/thumbnails

### Other STL thumnailers
- [stl-thumb](https://github.com/unlimitedbacon/stl-thumb/releases)
  - Open STL files with [../utilities/stl-as-thumb](../utilities/stl-as-thumb) to use it as a (static 2D) viewer.

## Regenerate thumbnails
To clear old thumbnails so new thumbnails are generated, the thumbnails must be cleared from "~/.cache/thumbnails".
