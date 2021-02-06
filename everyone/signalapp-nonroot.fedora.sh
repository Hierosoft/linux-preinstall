#!/bin/sh

# ^ from https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=signal-desktop-beta-bin
install_cmd=install_any.py
try_cmd="$HOME/git/linux-preinstall/utilities/install_any.py"
try2_cmd="$HOME/Downloads/git/linux-preinstall/utilities/install_any.py"
try3_cmd="$HOME/Downloads/git/poikilos/linux-preinstall/utilities/install_any.py"
install_cmd_path="`command -v $install_cmd`"
if [ ! -f "`command -v $install_cmd`" ]; then
    if [ -f "$try2_cmd" ]; then
        install_cmd="$try2_cmd"
    fi
    if [ -f "$try3_cmd" ]; then
        install_cmd="$try2_cmd"
    fi
    if [ -f "$try_cmd" ]; then
        install_cmd="$try_cmd"
    fi
    install_cmd_path="$install_cmd"
fi
if [ ! -f "$install_cmd_path" ]; then
    echo "ERROR: This script requires $install_cmd to be in the command path or one of the following:"
    echo " - $try_cmd"
    echo " - $try2_cmd"
    echo " - $try3_cmd"
    exit 1
fi

mkdir -p "$HOME/Downloads"
cd "$HOME/Downloads"
if [ $? -ne 0 ]; then
    echo "cd \"$HOME/Downloads\" failed."
    exit 1
fi
PKG_NAME="signal-desktop-beta_1.39.6-beta.1_amd64.deb"
if [ ! -f "$PKG_NAME" ]; then
    wget -O $PKG_NAME https://updates.signal.org/desktop/apt/pool/main/s/signal-desktop-beta/$PKG_NAME
fi
$install_cmd $PKG_NAME

cat <<END
If you do not have a smartphon and are not registered on Signal, you
must follow the directions at:

https://ctrl.alt.coop/en/post/signal-without-a-smartphone/

For adding the CAPTCHA code via terminal, see:

https://github.com/AsamK/signal-cli/wiki/Registration-with-captcha

Decoding the qrcode on Fedora requires zbarimg from zbar-tools:
  sudo dnf install -y zbar

Synchronizing contacts requires libunixsocket-java according to
https://ctrl.alt.coop/en/post/signal-without-a-smartphone/
but it shows no error message without it. Try installing Java then:
  wget http://www.matthew.ath.cx/projects/java/libmatthew-java-0.8.1.tar.gz
  tar -xf libmatthew-java-0.8.1.tar.gz
  cd libmatthew-java-0.8.1
  # Alternatively, https://github.com/tomerf/libunixsocket-java
  # may work.
  # The make command further down requires javac, so install the devel
  # package:
  sudo dnf install -y java-latest-openjdk-devel
  sudo dnf install -y java-latest-openjdk
  # ensure Java 11 or higher so is present: java --version
  # if not, try installing java-11-openjdk. Alessio
  # (https://ask.fedoraproject.org/t/javac-not-found/2027/3)
  # says to ensure 11 is installed.
  # then as per http://www.matthew.ath.cx/projects/java/INSTALL run:
  make
  sudo make install
  

If you have a smartphone, simply open Signal Desktop and scan the 
QR-code using your phone's Signal app.
END

exit 0


# ONLY if from source:


GIT_URL=https://github.com/signalapp/Signal-Desktop.git
mkdir -p "$HOME/Downloads/git/signalapp"
cd "$HOME/Downloads/git/signalapp"
if [ $? -ne 0 ]; then
    echo "cd \"$HOME/Downloads/git/signalapp\" failed."
    exit 1
fi
if [ ! -d Signal-Desktop ]; then
    git clone $GIT_URL
    if [ $? -ne 0 ]; then
        echo "ERROR: 'git clone $GIT_URL' failed."
        exit 1
    fi
    cd Signal-Desktop
else
    cd Signal-Desktop
    git pull
    if [ $? -ne 0 ]; then
        echo "WARNING: 'git pull' failed in \"`pwd`\"."
    fi
fi
