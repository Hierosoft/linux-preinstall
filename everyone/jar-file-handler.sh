#!/bin/bash
cd "`dirname "$0"`"
cd ../utilities
./install_any.py jar-run.sh "Jar Run"
cat <<END

Manual steps are necessary:
1. Right-click a jar file.
2. Click "Open With Other Application..."
3. Check "Use as default for this kind of file."
4. Scroll down to "Jar Run" and select it then press "Open"
   (If you checked the box in step 3, double-click should work afterward).

END
