#!/bin/bash
source /opt/ros/noetic/setup.bash
source ~/catkin_fs/devel/setup.bash
bash -c "python3 ~/ros-bag-recorder/run.py"

exec $SHELL
