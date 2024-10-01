#!/bin/bash
sudo apt update -y

if [ ! -f "`command -v pyenv`" ]; then
    sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

    curl https://pyenv.run | bash

    if grep -q 'PYENV_ROOT' ~/.bashrc; then
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
    else
        echo "PYENV_ROOT is not present in ~/.bashrc. Skipping changes."
    fi

fi

pyenv install 2.7.18 | exit $?
pyenv global 2.7.18 | exit $?
# ^ set python to python2 like the olden days of 2023 ;)
