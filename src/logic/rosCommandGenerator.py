"""
Generate a rosbag record command based on the given parameters
"""

from typing import List, Dict, Tuple

import datetime

from ..constants import Constants


def generateRosBagRecordCommand(
    topicList: List[str], prefix: str, options: Dict[str, str]
) -> Tuple[str, str]:
    """
    Generate a rosbag record command based on the given parameters

    parameters
    ----------
    topicList : List[str]
        List of topics to record
    options : Dict[str, str]
        Dictionary of options to use when generating the command

    returns
    -------
    Tuple[str, str]
        The generated command, and the bag name
    """

    currentTime = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

    command = "ros2 bag record"

    command += f" -o {Constants.BAG_DIR_PATH}"
    if prefix != "":
        command += prefix + "_" + currentTime

    for key, value in options.items():
        command += " " + key + " " + value

    for topic in topicList:
        command += " " + topic

    return command, prefix + "_" + currentTime + ".bag"
