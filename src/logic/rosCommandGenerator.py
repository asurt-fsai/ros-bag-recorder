"""
Generate a rosbag record command based on the given parameters
"""

from typing import List, Dict

import os


def generateRosBagRecordCommand(topicList: List[str], prefix: str, options: Dict[str, str]) -> str:
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
    str
        The generated command
    """

    path = os.path.expanduser("~/bags/")

    command = "rosbag record"

    command += f" -o {path}"
    if prefix != "":
        command += prefix

    for key, value in options.items():
        command += " " + key + " " + value

    for topic in topicList:
        command += " " + topic

    return command
