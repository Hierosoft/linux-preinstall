#!/bin/sh

echo "This script"
../utilities/blender-install-git-addon.sh https://github.com/machin3io/MACHIN3tools.git

cat <<END
Manually install and enable:
- Pie menus (works well with MACHIN3tools)

Manually enable built-in:
- Loop Tools
- TinyCAD
- 3D Print Toolbox

Paid ones that may be helpful:
- HardOps: hard surface modeling shortcuts
- boxcutter: https://blendermarket.com/products/boxcutter

END
