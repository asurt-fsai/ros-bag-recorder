"""
This file contains all the constants used in the project.
"""
import os
from enum import Enum


class Constants:  # pylint: disable=R0903
    """
    Constants
    """

    # pylint: disable=C0103

    IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
    BAG_DIR_PATH = os.path.expanduser("~/bags/")
    JSON_FILE_NAME = "description.json"


class Pages(Enum):
    """
    Pages Enum
    """

    RECORD = 1
    AVAILABLE_BAGS = 2
