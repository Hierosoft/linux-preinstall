#!/bin/sh
if [ -z "$G_P_INSTALLER_PATH" ]; then
	for TRY_GPI_PATH in "`command -v install-geany-plugin.sh`" `pwd`/../utilities/install-geany-plugin.sh `pwd`/utilities/install-geany-plugin.sh $HOME/git/linux-preinstall $HOME/Downloads/git/linux-preinstall
	do
		if [ -f "$TRY_GPI_PATH" ]; then
			G_P_INSTALLER_PATH="$TRY_GPI_PATH"
			break
		#else
		#	echo "$TRY_GPI_PATH does not exist."
		fi
	done
fi
if [ ! -f "$G_P_INSTALLER_PATH" ]; then
	echo "The location of install-geany-plugin.sh was not detected."
	echo
	opener=""
	if [ -z "$G_P_INSTALLER_PATH" ]; then
		opener="Set G_P_INSTALLER_PATH or"
	else
		echo "mkdir -p ~/git && git clone https://github.com/poikilos/linux-preinstall ~/git"
		echo
		opener="to"
	fi
	echo "$opener clone or extract the linux-preinstall repo to $HOME/Downloads/git/linux-preinstall or $HOME/git/linux-preinstall"
	exit 1
fi
echo "* running $G_P_INSTALLER_PATH addons..."
$G_P_INSTALLER_PATH addons
