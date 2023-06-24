"""
Generate a rosbag record command based on the given parameters
"""

from typing import List, Dict

from ..constants import Constants


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

    command = "rosbag record"

    command += f" -o {Constants.BAG_DIR_PATH}"
    if prefix != "":
        command += prefix

    for key, value in options.items():
        command += " " + key + " " + value

    for topic in topicList:
        command += " " + topic

    return command
