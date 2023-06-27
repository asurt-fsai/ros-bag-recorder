#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source /opt/ros/noetic/setup.bash
bash -c "python3 "$SCRIPT_DIR"/run.py"

exec $SHELL
