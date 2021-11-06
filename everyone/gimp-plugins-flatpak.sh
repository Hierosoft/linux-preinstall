#!/bin/bash
#sudo flatpak install org.gimp.GIMP org.gimp.GIMP.Plugin.Resynthesizer org.gimp.GIMP.Plugin.LiquidRescale org.gimp.GIMP.Plugin.Lensfun org.gimp.GIMP.Plugin.GMic org.gimp.GIMP.Plugin.Fourier org.gimp.GIMP.Plugin.FocusBlur org.gimp.GIMP.Plugin.BIMP
# ^ Asks:
cat > /dev/null <<END
Found similar ref(s) for ‘org.gimp.GIMP’ in remote ‘flathub’ (system).
Use this remote? [Y/n]: y
Skipping: org.gimp.GIMP/x86_64/stable is already installed
Similar refs found for ‘org.gimp.GIMP.Plugin.Resynthesizer’ in remote ‘flathub’ (system):

   1) runtime/org.gimp.GIMP.Plugin.Resynthesizer/x86_64/2-3.36
   2) runtime/org.gimp.GIMP.Plugin.Resynthesizer/x86_64/2-40

Which do you want to use (0 to abort)? [0-2]: 2
END

sudo flatpak install -y flathub org.gimp.GIMP org.gimp.GIMP.Plugin.Resynthesizer/x86_64/2-40 org.gimp.GIMP.Plugin.LiquidRescale/x86_64/2-40 org.gimp.GIMP.Plugin.Lensfun/x86_64/2-40 org.gimp.GIMP.Plugin.GMic/x86_64/2-40 org.gimp.GIMP.Plugin.Fourier/x86_64/2-40 org.gimp.GIMP.Plugin.FocusBlur/x86_64/2-40 org.gimp.GIMP.Plugin.BIMP/x86_64/2-40
