#!/usr/bin/env bash
set -e

SELF_DIR="$( cd $( dirname "${BASH_SOURCE[0]}" ) && pwd )"

source $SELF_DIR/.virtualenv/bin/activate

python $SELF_DIR/windowbox-barker.py
