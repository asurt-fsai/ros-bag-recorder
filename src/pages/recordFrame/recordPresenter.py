"""
FTP Client Presenter
"""
from __future__ import annotations
from typing import Optional, Protocol, Callable, Any, List, Dict

import re
import os
import subprocess
import signal
import shlex

import tkinter as tk
import psutil
from ...logic.rosCommandGenerator import generateRosBagRecordCommand


class RecordView(Protocol):
    """
    View Protocol
    """

    # pylint: disable=C0116

    def buildGUI(self, presenter: RecordPresenter, rosTopics: List[str]) -> None:
        ...

    @property
    def prefix(self) -> str:
        ...

    @property
    def durationOption(self) -> str:
        ...

    @property
    def numberOption(self) -> str:
        ...

    @property
    def selectedTopicTypeOption(self) -> str:
        ...

    @property
    def checkedTopics(self) -> List[str]:
        ...

    @property
    def command(self) -> str:
        ...

    def after(self, time: int, func: Callable[..., None]) -> None:
        ...

    def updateTopicsByDropDownList(self, name: str) -> None:
        ...

    def updateTerminalResponse(self, response: str) -> None:
        ...

    def updateCommandResponse(self, command: str) -> None:
        ...

    def scrollDownTerminalResponse(self) -> None:
        ...

    def disableUiOnRecord(self) -> None:
        ...

    def enableUiOnStopRecord(self) -> None:
        ...


class RecordPresenter:
    """
    Record Presenter
    """

    # pylint: disable=W0613

    def __init__(self, view: RecordView) -> None:
        self.view = view
        self.isCommandValid = False
        self.proc: Any = None
        self.stdoutData = ""

    def handleStartRecord(self, event: Optional[tk.EventType] = None) -> None:
        """
        handle start record the ros bag
        The function creates a new subprocess that runs the command
        While this function is running the GUI is disabled
        """

        if not self.isCommandValid:
            self.view.updateCommandResponse("Build command first")
            return

        if not os.path.exists(os.path.expanduser("~/bags/")):
            os.makedirs(os.path.expanduser("~/bags/"))

        command = shlex.split(self.view.command)
        self.proc = subprocess.Popen(  # pylint: disable=R1732
            command, stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )

        topicListStr = "\n".join(self.view.checkedTopics)
        printOutput = f"""Started Recording a bag of the following topics:\n{topicListStr}\n\n
        The bag can be found in the following directory:\n{os.path.expanduser("~/bags/")}\n\n"""

        self.view.disableUiOnRecord()
        self.view.updateTerminalResponse(printOutput)
        self.view.scrollDownTerminalResponse()

    def handleStopRecord(self, event: Optional[tk.EventType] = None) -> None:
        """
        handle stop record the ros bag
        The function stops the process that is running the record bag command
        This function returns the GUI to normal
        """

        for proc in psutil.process_iter():
            if "record" in proc.name() and set(self.view.command[2:]).issubset(proc.cmdline()):
                proc.send_signal(signal.SIGINT)

        self.proc.send_signal(signal.SIGINT)

        printOutput = "Stopped Recording\n\n"
        self.view.enableUiOnStopRecord()
        self.view.updateTerminalResponse(printOutput)
        self.view.scrollDownTerminalResponse()

    def handleCheckTopicsByDropDownList(self, event: Optional[tk.EventType] = None) -> None:
        """
        Check the topics by the drop down list
        """
        self.view.updateTopicsByDropDownList(self.view.selectedTopicTypeOption)

    def handleGenerateCommand(self, event: Optional[tk.EventType] = None) -> None:
        """
        Given the selected topics and options, generate the command
        """

        self.isCommandValid = False
        ### validate checked topics ###
        if len(self.view.checkedTopics) == 0:
            self.view.updateCommandResponse("No topics selected")
            return

        ### validate prefix ###
        if self.view.prefix == "":
            self.view.updateCommandResponse("No prefix entered")
            return

        if not re.match(r"^[a-zA-Z0-9_.-]+$", self.view.prefix):
            self.view.updateCommandResponse("Invalid prefix, should be alphanumeric")
            return

        ### validate options ###
        options: Dict[str, str] = {}

        if self.view.durationOption != "":
            if re.match(r"\d+$", self.view.durationOption) or re.match(
                r"\d+[mhMH]$", self.view.durationOption
            ):
                options["--duration"] = self.view.durationOption
            else:
                self.view.updateCommandResponse(
                    "Invalid duration format, should be number or number followed with m or h"
                )
                return

        if self.view.numberOption != "":
            if re.match(r"\d+$", self.view.numberOption):
                options["--limit"] = self.view.numberOption
            else:
                self.view.updateCommandResponse("Invalid number format, should be number")
                return

        ### generate command ###
        command = generateRosBagRecordCommand(self.view.checkedTopics, self.view.prefix, options)
        self.view.updateCommandResponse(command)
        self.isCommandValid = True

    def run(self) -> None:
        """
        Run the GUI.
        """

        command = shlex.split("rostopic list")
        proc = subprocess.Popen(  # pylint: disable=R1732
            command, stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )

        out, _ = proc.communicate()

        topics = out.decode("utf-8").strip().split("\n")

        self.view.buildGUI(self, topics)
