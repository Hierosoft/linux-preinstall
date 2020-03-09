#!/bin/bash

if [ "@$1" = "@postinstall" ]; then
    # The non-root script calls this script with this option.
    echo "Running post-install..."
    mkdir -p /etc/borg/{keys,ssh}
    mkdir -p /var/lib/borg/{cache,security}

elif [ "@$1" = "@client" -o "@$1" = "@server" ]; then
    echo "Running preinstall..."
    sudo apt install -y python3 python3-dev python3-pip python-virtualenv \
        libssl-dev openssl \
        libacl1-dev libacl1 \
        build-essential
    sudo apt install -y libfuse-dev fuse pkg-config  # optional, for FUSE support
else
    echo "You must first run ./borg-server-nonroot.sh on the server, then run this script with the client option."
fi
