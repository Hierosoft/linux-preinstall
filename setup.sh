#!/bin/bash
python3 setup-bash-tools.py "$@"
code=$?
if [ $code -ne 0 ]; then exit $code; fi

