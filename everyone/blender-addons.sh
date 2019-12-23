#!/bin/sh

#echo "This script"
../utilities/blender-install-git-addon.sh https://github.com/machin3io/MACHIN3tools.git
../utilities/blender-install-git-addon.sh https://github.com/JacquesLucke/code_autocomplete.git
../utilities/blender-install-git-addon.sh https://github.com/jayanam/fast-carve.git

cat <<END
## Manual Steps Required
- You must manually enable the addons above in User Preferences,
  Add-ons to use them.
- Click "Save User Preferences" if you don't want to have to
  enable each Add-on again for each Blender project (blend
  file).
- If you want to use **code_autocomplete**, after enabling it
  above, you must also:
  - Open a text editor panel
  - Open the left menu (with the small plus button at the left edge
    of the Text Editor panel, near the top).
  - Enable Line Numbers, Word Wrap, and Syntax Highlight
  - Under "Addon Development," choose "code_autocomplete"
  - Click Run Addon, Start
  - Click Build if there is a warning (usually necessary for
    first-time setup).

## Optional
There are some addons on the Blender Market you may find helpful for
simplifying the modeling of advanced shapes:
- [Boxcutter](https://blendermarket.com/products/boxcutter)
  Price: ~$20
  Description: Easily add many shapes of divots and protrusions, such
    as using freehand shape drawing and arrays.
- [Bezier Mesh Shaper](https://blendermarket.com/products/bezier-mesh-shaper)
  Price: ~9.99
  Description: Deform parts of a mesh using bezier curves.
- [EdgeFlow](https://blenderartists.org/t/it-is-finally-here-edge-flow-set-flow-for-blender-benjamin-saunder/1128115)
  Price: free of charge
  Description: Reflow multiple edge loops, making spacing and curve smooth.
  Install: "../utilities/blender-install-git-addon.sh https://github.com/BenjaminSauder/EdgeFlow.git"
  Alternatives: mifthtools (formerly Miratools)
- [Hardops](https://blendermarket.com/products/hardopsofficial)
  Price: ~$20
  Description: hard surface modeling shortcuts
- Meshmachine ~~https://blendermarket.com/products/MESHmachine~~
  Price: name your price
  Description: no longer on Blender Market
    See instead:
    <https://gumroad.com/l/MESHmachine#>
- [mifthtools](https://blenderartists.org/t/miratools/637385)
  Price: Free
  Install: "../utilities/blender-install-git-addon.sh https://github.com/mifth/mifthtools"
  Description: (formerly Mira Tools) Linear deform, curve stretch,
    model along surfaces (see also [mifthtools
    wiki](https://github.com/mifth/mifthtools/wiki))
- [Sculpt Toolkit](https://blendermarket.com/products/sculpttkt---a-tool-kit-for-sculptors)
  Price: ~$15
  Rating: 4/5
  Description: Metaball-like but detailed modeling
  Alternatives: Speedsculpt
- [Speedsculpt](https://blendermarket.com/products/speedsculpt)
  Price: ~$15
  Rating: 5/5
  Description: Metaball-like but detailed modeling, cut curves,
    and other features for highly-detailed models. Add eyebrows or hair
    by drawing a freehand outline on the surface.
  Alternatives: Sculpt Toolkit
- [Car-Rig Pro "Blender Kit"](https://blendermarket.com/products/car-rig-pro-blender-kit)
  Price: $39
  Rating: 4/5
  Description: Draw a curve, and the addon animates the car, snaps the
    wheels to the curve, and handles all physics.
- [Procedural Noise Pack](https://gumroad.com/l/NOISE-P)
  Author: Simon Thommes
  Price: Pay what you want
  Description: (recommended by CGShrimp [3D Nebulae and the Power of the
    Blender Community - Gleb
    Alexandrov](https://www.youtube.com/watch?v=4w8_SBxCOxo&t=0s)
- [MandelBulb (blend file)]
  Author: Gleb Alexandrov @gleb_alexandrov
  Description: See JonasDichelle's tweaked MandelBulb in
    "everyone/blender/mandelbulb (1) by JonasDichelle.blend"
    from https://drive.google.com/file/d/1OZbh7f4KIFVMgzIEP_cenCQp-36RwozW/view
    via https://www.youtube.com/watch?v=WSQFt1Nruns
- [Volumetric cycles #b3d nebula 2.0]
  Author: Robert @robert_trirop
  Description: infinitely complex nebulae
    https://twitter.com/robert_trirop/status/755141408302956545

END

cat <<END
Manually install and enable:
- Pie menus (works well with MACHIN3tools)
  - built into Blender >=2.8

Manually enable built-in:
- Loop Tools
- TinyCAD
- 3D Print Toolbox

END
