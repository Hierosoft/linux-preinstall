#!/bin/bash
#compatibility:
dnf -y msttcore-fonts wine-fonts wine-tahoma-fonts-system wine-times-new-roman-fonts-system wine-wingdings-fonts-system

source_fonts_path=/usr/share/wine/fonts
this_font_name=arial.ttf
this_font_path="$source_fonts_path/$this_font_name"
my_fonts_path=/usr/local/share/fonts/wine
if [ -f "$this_font_path" ]; then
  if [ ! -d "$my_fonts_path" ]; then
    sudo mkdir -p "$my_fonts_path"
  fi
  this_dest_path="$my_fonts_path/$this_font_name"
  if [ ! -f "$this_dest_path" ]; then
    if [ ! -L "$this_dest_path" ]; then
      echo "making symlink to $this_font_path..."
      sudo ln -s "$this_font_path" "$this_dest_path"
    else
      echo "NOTICE: redoing existing symlink $this_dest_path"
      sudo rm -f "$this_dest_path"
      sudo ln -s "$this_font_path" "$this_dest_path"
    fi
  else
    if [ ! -L "$this_dest_path" ]; then
      echo "WARNING: skipping font symlink $this_dest_path which is already a real file"
    else
      echo "NOTICE: redoing existing symlink $this_dest_path"
      sudo rm -f "$this_dest_path"
      sudo ln -s "$this_font_path" "$this_dest_path"
    fi
  fi
else
  echo "WARNING, font not present: $this_font_path"
fi

#also: wine-fonts wine-tahoma-fonts-system wine-times-new-roman-fonts-system wine-wingdings-fonts-system
#wine-*-system: wine font families system integration
#Calibri and Cambria compatible fonts (are installed by default?) respectively are:
sudo dnf -y install google-crosextra-carlito-fonts google-crosextra-caladea-fonts
#Make substitutions in libreoffice (see https://ask.libreoffice.org/en/question/15041/calibri-and-cambria-fonts-in-libreoffice/ which links to https://wiki.debian.org/SubstitutingCalibriAndCambriaFonts):

# * should already be in /etc/fonts/conf.d/
# * but will not work on new documents, only documents created on a computer with Calibri and Cambria
#Rename them (see https://superuser.com/questions/472102/change-font-family-rename-font):
sudo dnf -y install fontforge
# * open fontforge (gui)
if [ ! -d "$HOME/tmp/google-crosextra-carlito-as-calibri" ]; then

  mkdir -p "$HOME/tmp/google-crosextra-caladea-as-cambria"
  cp /usr/share/fonts/google-crosextra-caladea/* "$HOME/tmp/google-crosextra-caladea-as-cambria/"
  cd "$HOME/tmp/google-crosextra-caladea-as-cambria"
  mv Caladea-BoldItalic.ttf Cambria-BoldItalic.ttf
  mv Caladea-Bold.ttf Cambria-Bold.ttf
  mv Caladea-Italic.ttf Cambria-Italic.ttf
  mv Caladea-Regular.ttf Cambria-Regular.ttf

  mkdir -p "$HOME/tmp/google-crosextra-carlito-as-calibri"
  cp /usr/share/fonts/google-crosextra-carlito/* "$HOME/tmp/google-crosextra-carlito-as-calibri/"
  cd "$HOME/tmp/google-crosextra-carlito-as-calibri"
  mv Carlito-BoldItalic.ttf Calibri-BoldItalic.ttf
  mv Carlito-Bold.ttf Calibri-Bold.ttf
  mv Carlito-Italic.ttf Calibri-Italic.ttf
  mv Carlito-Regular.ttf Calibri-Regular.ttf

  # * fontforge "$HOME/tmp/google-crosextra-carlito-as-calibri/"
  # * fontforge "$HOME/tmp/google-crosextra-caladea-as-cambria"
  # * manually change names using fontforge or TTFEdit (java) or fpedit (Windows) from https://www.microsoft.com/typography/property/fpedit.htm
fi
  # * Element, Font Info...
