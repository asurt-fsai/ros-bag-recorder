#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PYTHON_SUFFIX="3"

sudo apt update
sudo apt-get install --no-install-recommends -y \
    python$PYTHON_SUFFIX-pip \
    pre-commit \
    wget \
    $ADDITIONAL_PACKAGES


pip$PYTHON_SUFFIX install --upgrade pip$PYTHON_SUFFIX
pip$PYTHON_SUFFIX install --upgrade customtkinter
pip$PYTHON_SUFFIX install -r $SCRIPT_DIR/requirements.txt

chmod +x $SCRIPT_DIR/.hooks/install_hooks.sh
$SCRIPT_DIR/.hooks/install_hooks.sh
chmod +x $SCRIPT_DIR/run.sh
