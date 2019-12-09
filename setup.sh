#!/usr/bin/env bash
set -e

VENV=venv

if [ ! -d $VENV ]; then
    PYTHON=`which python3.5`

    if [ -f $PYTHON ]; then
        virtualenv -p $PYTHON $VENV
    else
        echo "could not find python3.7"
    fi
fi

. $VENV/bin/activate

pip3 install -r requirements.txt
