#!/usr/bin/env bash
set -e

SELF_DIR="$( cd $( dirname "${BASH_SOURCE[0]}" ) && pwd )"

cd "$SELF_DIR"

# Python components
rm -rf ./.virtualenv
virtualenv --always-copy ./.virtualenv
source ./.virtualenv/bin/activate
pip install --upgrade pip
pip install -r ./reqs.txt
deactivate
