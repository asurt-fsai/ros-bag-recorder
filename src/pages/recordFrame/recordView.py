"""
Record page
"""

from typing import Dict, Any, Union, Optional, Protocol, List

import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image

from ...components.scrollableCheckBoxFrame import ScrollableCheckBoxFrame
from ...constants import Constants


class RecordPresenter(Protocol):
    """
    Record Presenter protocol
    """

    # pylint: disable=C0116

    def handleStartRecord(self, event: Optional[tk.EventType] = None) -> None:
        ...

    def handleStopRecord(self, event: Optional[tk.EventType] = None) -> None:
        ...

    def handleCheckTopicsByDropDownList(self, event: Optional[tk.EventType] = None) -> None:
        ...

    def handleGenerateCommand(self, event: Optional[tk.EventType] = None) -> None:
        ...

    def handleRefreshTopic(self, event: Optional[tk.EventType] = None) -> None:
        ...


class RecordView(ctk.CTkFrame):  # type: ignore # pylint: disable=R0901
    """
    Record frame
    """

    def __init__(self, master: Union[ctk.CTk, ctk.CTkFrame], **kwargs: Optional[Any]) -> None:
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.widgets: Dict[str, ctk.CTkBaseClass] = {}

    def buildGUI(self, presenter: RecordPresenter, rosTopics: List[str]) -> None:
        """
        Build the GUI, runs all the methods that build the GUI.
        """
        self.buildScrollableFrameBar(presenter, rosTopics)
        self.buildMainSection(presenter)
        self.buildOptionsSection(presenter)

    def buildScrollableFrameBar(self, presenter: RecordPresenter, rosTopics: List[str]) -> None:
        """
        build the scrollable frame bar
        it contains both a dropdown menu and a scrollable frame with checkboxes for topic list
        """
        scrollableBarFrame = ctk.CTkFrame(self, width=250, corner_radius=0)
        scrollableBarFrame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="ns")
        scrollableBarFrame.grid_columnconfigure(0, weight=1)
        scrollableBarFrame.grid_rowconfigure(1, weight=1)

        topicSelectOptions = ctk.CTkOptionMenu(
            scrollableBarFrame,
            dynamic_resizing=True,
            command=presenter.handleCheckTopicsByDropDownList,
            values=[
                "none",
                "all",
                "perception",
                "slam",
                "supervisor",
                "control",
                "planning",
                "lidar",
            ],
        )
        topicSelectOptions.grid(row=0, column=0, padx=(10, 5), pady=(5, 5), sticky="we")
        self.widgets["topicSelectOptions"] = topicSelectOptions

        refreshImage = ctk.CTkImage(
            light_image=Image.open(os.path.join(Constants.IMAGE_PATH, "refresh_dark.png")),
            dark_image=Image.open(os.path.join(Constants.IMAGE_PATH, "refresh_dark.png")),
            size=(20, 20),
        )

        refreshButton = ctk.CTkButton(scrollableBarFrame, text="", width=50, image=refreshImage)
        refreshButton.configure(command=presenter.handleRefreshTopic)
        refreshButton.grid(row=0, column=1, pady=(5, 5), padx=(5, 10), sticky="e")

        scrollableCheckBoxes = ScrollableCheckBoxFrame(
            scrollableBarFrame,
            items=rosTopics,
            command=presenter.handleGenerateCommand,
            width=300,
        )
        scrollableCheckBoxes.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ns"
        )
        self.widgets["scrollableCheckBoxes"] = scrollableCheckBoxes

    def buildMainSection(self, presenter: RecordPresenter) -> None:
        """
        Build the response section frame with widgets
        The response section contain the terminal response and the directory list text boxes
        """
        mainSectionFrame = ctk.CTkFrame(self)
        mainSectionFrame.grid(row=0, column=1, sticky="nsew", padx=(5, 5), pady=(10, 10))
        mainSectionFrame.grid_columnconfigure((0, 2), weight=1)
        mainSectionFrame.grid_rowconfigure(5, weight=1)

        terminalResponseLabel = ctk.CTkLabel(mainSectionFrame, text="Terminal Response")
        terminalResponseLabel.grid(
            row=0, column=0, columnspan=5, padx=(10, 10), pady=(10, 10), sticky="wns"
        )
        terminalResponseTextbox = ctk.CTkTextbox(mainSectionFrame, height=250)
        terminalResponseTextbox.grid(
            row=1, column=0, columnspan=5, padx=(10, 10), pady=(10, 10), sticky="nsew"
        )
        terminalResponseTextbox.configure(state="disabled")
        self.widgets["terminalResponseTextbox"] = terminalResponseTextbox

        prefixEntry = ctk.CTkEntry(
            mainSectionFrame,
            placeholder_text="Prefix for bag name, final name will be {prefix}{timestamp}.bag",
            validate="focus",
            validatecommand=presenter.handleGenerateCommand,
        )
        prefixEntry.grid(row=2, column=0, columnspan=3, padx=20, pady=(10, 0), sticky="nsew")
        self.widgets["prefixEntry"] = prefixEntry
        prefixEntry.bind("<KeyRelease>", presenter.handleGenerateCommand)

        startButton = ctk.CTkButton(
            mainSectionFrame, command=presenter.handleStartRecord, text="Start Recording"
        )
        startButton.grid(row=2, column=3, padx=20, pady=10, sticky="nsew")
        self.widgets["startButton"] = startButton

        stopButton = ctk.CTkButton(
            mainSectionFrame, command=presenter.handleStopRecord, text="Stop Recording"
        )
        stopButton.configure(state="disabled")
        stopButton.grid(row=2, column=4, padx=20, pady=10, sticky="nsew")
        self.widgets["stopButton"] = stopButton

        commandLabel = ctk.CTkLabel(mainSectionFrame, text="Generated rosbag command")
        commandLabel.grid(row=3, column=0, columnspan=5, padx=(10, 10), pady=(20, 20), sticky="wns")
        commandTextbox = ctk.CTkTextbox(mainSectionFrame, height=150)
        commandTextbox.grid(
            row=4, column=0, columnspan=5, padx=(10, 10), pady=(0, 20), sticky="nsew"
        )
        commandTextbox.configure(state="disabled")
        commandTextbox.bind("<Button-1>", commandTextbox.focus_set())
        commandTextbox.bind("<Control-c>", self._copy)
        self.widgets["commandTextbox"] = commandTextbox

        copyButton = ctk.CTkButton(mainSectionFrame, command=lambda: self._copy(None), text="Copy")
        copyButton.grid(row=5, column=4, padx=20, pady=3, sticky="n")
        self.widgets["stopButton"] = stopButton

    def buildOptionsSection(self, presenter: RecordPresenter) -> None:
        """
        build the options section frame for the rosbag command
        """

        optionFrame = ctk.CTkFrame(self)
        optionFrame.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="nswe")

        optionsLabel = ctk.CTkLabel(master=optionFrame, text="Enter rosbag options")
        optionsLabel.grid(row=0, column=0, columnspan=1, padx=10, pady=(10, 20), sticky="n")

        numberLabel = ctk.CTkLabel(master=optionFrame, text="Number of messages", anchor="w")
        numberLabel.grid(row=2, column=0, padx=10, sticky="nw")
        numberEntry = ctk.CTkEntry(
            master=optionFrame,
            width=200,
        )
        numberEntry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="n")
        self.widgets["numberEntry"] = numberEntry
        numberEntry.bind("<KeyRelease>", presenter.handleGenerateCommand)

        durationLabel = ctk.CTkLabel(
            master=optionFrame, text="Duration e.g. (30, 1m, 2h)", anchor="w"
        )
        durationLabel.grid(row=4, column=0, padx=10, sticky="nw")
        durationEntry = ctk.CTkEntry(
            master=optionFrame,
            width=200,
        )
        durationEntry.grid(row=5, column=0, padx=5, sticky="n")
        self.widgets["durationEntry"] = durationEntry
        durationEntry.bind("<KeyRelease>", presenter.handleGenerateCommand)

    def _copy(self, _: Any) -> None:
        """
        copy the command to clipboard
        """
        self.clipboard_clear()
        self.clipboard_append(self.command)
        self.update()

    @property
    def prefix(self) -> str:
        """
        Get the input from the prefix entry widget

        returnsdisableUiOnRecord
        -------
        str
            The prefix input
        """
        return self.widgets["prefixEntry"].get()  # type: ignore

    @property
    def command(self) -> str:
        """
        Get the input from the command entry widget

        returns
        -------
        str
            The commandTextbox input
        """
        return self.widgets["commandTextbox"].get("1.0", "end")  # type: ignore

    @property
    def durationOption(self) -> str:
        """
        Get the input from the duration entry widget

        returns
        -------
        str
            The duration input
        """
        return self.widgets["durationEntry"].get()  # type: ignore

    @property
    def numberOption(self) -> str:
        """
        Get the input from the number entry widget

        returns
        -------
        str
            The number input
        """
        return self.widgets["numberEntry"].get()  # type: ignore

    @property
    def selectedTopicTypeOption(self) -> str:
        """
        Get the input from the topic type widget

        returns
        -------
        str
            The size input
        """
        return self.widgets["topicSelectOptions"].get()  # type: ignore

    @property
    def checkedTopics(self) -> List[str]:
        """
        Get the checked topics from the topics list frame

        returns
        -------
        List[str]
            The checked topics
        """
        return self.widgets["scrollableCheckBoxes"].getCheckedItems()  # type: ignore

    def updateTopicsByDropDownList(self, name: str) -> None:
        """
        Update the topics list by the drop down list
        """

        if name == "all":
            self.widgets["scrollableCheckBoxes"].selectAll()
        elif name == "none":
            self.widgets["scrollableCheckBoxes"].deselectAll()
        else:
            self.widgets["scrollableCheckBoxes"].selectContainingName(name)

    def scrollDownTerminalResponse(self) -> None:
        """
        Scroll the terminal response textbox down
        """
        self.widgets["terminalResponseTextbox"].see("end")

    def updateTerminalResponse(self, response: str) -> None:
        """
        Update the terminal response textbox with the response
        The

        parameters
        ----------
        response: str
            The response to update the textbox with
        """
        self.widgets["terminalResponseTextbox"].configure(state="normal")
        self.widgets["terminalResponseTextbox"].insert("end", response)
        self.widgets["terminalResponseTextbox"].configure(state="disabled")

    def updateCommandResponse(self, command: str) -> None:
        """
        Update the command response textbox with the command
        The text is replaced with the command

        parameters
        ----------
        command: str
            The command to update the textbox with
        """
        self.widgets["commandTextbox"].configure(state="normal")
        self.widgets["commandTextbox"].delete(1.0, "end")
        self.widgets["commandTextbox"].insert("end", command)
        self.widgets["commandTextbox"].configure(state="disabled")

    def disableUiOnRecord(self) -> None:
        """
        Disable the UI when recording
        """

        self.widgets["startButton"].configure(state="disabled")
        self.widgets["stopButton"].configure(state="normal")
        self.widgets["prefixEntry"].configure(state="disabled")
        self.widgets["durationEntry"].configure(state="disabled")
        self.widgets["numberEntry"].configure(state="disabled")
        self.widgets["topicSelectOptions"].configure(state="disabled")

    def enableUiOnStopRecord(self) -> None:
        """
        Enable the UI when recording
        """

        self.widgets["startButton"].configure(state="normal")
        self.widgets["stopButton"].configure(state="disabled")
        self.widgets["prefixEntry"].configure(state="normal")
        self.widgets["durationEntry"].configure(state="normal")
        self.widgets["numberEntry"].configure(state="normal")
        self.widgets["topicSelectOptions"].configure(state="normal")

    def emptyTopicCheckList(self) -> None:
        """
        Empty the topic check list
        """
        self.widgets["scrollableCheckBoxes"].removeAllItems()

    def addTopicsToCheckList(self, topics: List[str]) -> None:
        """
        Add topics to the check list

        parameters
        ----------
        topics: List[str]
            The topics to add to the check list
        """
        self.widgets["scrollableCheckBoxes"].addItems(topics)
