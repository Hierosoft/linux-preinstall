#!/bin/bash
# Tested with Monero on Ubuntu
if [ "@$srcName" = "@" ]; then
    srcName=monero-wallet-gui.AppImage    
fi
if [ "@$dstName" = "@" ]; then
    dstName=monero-wallet-gui.AppImage
fi
if [ "@$DST_DIR" = "@" ]; then
    DST_DIR="/media/owner/SEAN16A/monero-gui"
fi

printf "* backing up \"$0\" to \"$DST_DIR\" from \"`pwd`\"..."
cp "$0" "$DST_DIR/"
if [ $? -ne 0 ]; then
    echo "FAILED"
else
    echo "OK"
fi

cd ~/Downloads
if [ ! -z "`ps -e | grep monero`" ]; then
    echo "First, close:"
    ps -e | grep onero
    echo "Such as by using these steps:"
    echo "* Open Monero GUI"
    echo "* Click the \"x\" (to exit the program)"
    echo "  * Choose \"Force stop\""
    exit 1
fi
EXT_NAME=`find . -type d -name "monero-gui*"`
if [ ! -d "$EXT_NAME" ]; then
    echo "Error: You must first extract the zipped monero-gui AppImage to a directory named like `pwd`/monero-gui*"
    exit 1
fi
cd "$EXT_NAME"
if [ $? -ne 0 ]; then
    echo "Error: 'cd \"$EXT_NAME\"' failed."
    exit 1
fi
if [ ! -f "$srcName" ]; then
    echo "Error: $srcName is missing in `pwd`"
    exit 1
fi
#killall $dstName
if [ ! -f "$srcName" ]; then
    echo "Error: $srcName is not present in `pwd`. Change the srcName variable to the name of the AppImage file in `pwd`."
    exit 1
fi

installFile(){
	src="$1"
	dst="$src"
	if [ ! -z "$2" ]; then
		dst="$2"
	fi
	mv -f "$src" "$DST_DIR/$dst"
	# ^ -f since the pdf documentation is readonly
	if [ $? -ne 0 ]; then
		echo "Error: After 'cd \"`pwd`\"', 'mv $src $DST_DIR/$dst' failed."
		exit 1
	fi
}
installFile LICENSE
installFile monerod
installFile monero-gui-wallet-guide.pdf
installFile monero-wallet-gui
mkdir -p "$DST_DIR/extras"
#mv extras/* "$DST_DIR/extras/"
#if [ $? -ne 0 ]; then
#	echo "Error: 'mv extras/* \"$DST_DIR/extras/\"' failed in `pwd`."
#	exit 1
#fi
installFile extras/monero-blockchain-ancestry                
installFile extras/monero-blockchain-stats
installFile extras/monero-blockchain-depth                  
installFile extras/monero-blockchain-usage
installFile extras/monero-blockchain-export                  
installFile extras/monero-gen-ssl-cert
installFile extras/monero-blockchain-import                  
installFile extras/monero-gen-trusted-multisig
installFile extras/monero-blockchain-mark-spent-outputs      
installFile extras/monero-wallet-cli
installFile extras/monero-blockchain-prune                   
installFile extras/monero-wallet-rpc
installFile extras/monero-blockchain-prune-known-spent-data
rmdir extras
if [ $? -ne 0 ]; then
	echo "Error: 'rmdir extras' failed in `pwd`."
	# exit 1
fi
# installFile $srcName $dstName
cd ..
if [ $? -ne 0 ]; then
	echo "'cd ..' failed in \"`pwd`\""
	cat <<END
Next do:
  rmdir "`pwd`"
END
	exit 1
fi
rmdir "$EXT_NAME"
if [ $? -ne 0 ]; then
	echo "Error: 'rmdir \"$EXT_NAME\"' failed in `pwd`."
	exit 1
fi
#cat <<END
#Next do:
#  cd "`pwd`"
#  rm -Rf "$EXT_NAME"
#END
echo Done
