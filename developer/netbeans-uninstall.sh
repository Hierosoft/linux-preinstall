#!/bin/bash

if [ "@$USER" = "@root" ]; then
	/usr/local/netbeans-8.2/uninstall.sh
else
	echo "The non-root install is not yet implemented."
fi
