"""
Record page
"""

from typing import Dict, Any, Union, Optional

import customtkinter as ctk

from .scrollableCheckBoxFrame import ScrollableCheckBoxFrame


class RecordFrame(ctk.CTkFrame):  # type: ignore # pylint: disable=R0901
    """
    Record frame
    """

    def __init__(self, master: Union[ctk.CTk, ctk.CTkFrame], **kwargs: Optional[Any]) -> None:
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 3), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.responseWidgets: Dict[str, ctk.CTkTextbox] = {}

        self.buildGUI()

    def buildGUI(self) -> None:
        """
        Build the GUI, runs all the methods that build the GUI.
        """
        self.buildScrollableFrameBar()
        self.buildMainSection()
        self.buildOptionsSection()

    def buildScrollableFrameBar(self) -> None:
        """
        build the scrollable frame bar
        it contains both a dropdown menu and a scrollable frame with checkboxes for topic list
        """
        scrollableBarFrame = ctk.CTkFrame(self, width=140, corner_radius=0)
        scrollableBarFrame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="ns")
        scrollableBarFrame.grid_rowconfigure(1, weight=1)

        topicSelectOptions = ctk.CTkOptionMenu(
            scrollableBarFrame,
            dynamic_resizing=True,
            values=[
                "perception",
                "slam",
                "supervisor",
                "control",
                "planning",
                "lidar",
                "all",
                "none",
            ],
        )
        topicSelectOptions.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="we")

        scrollableCheckBoxes = ScrollableCheckBoxFrame(
            scrollableBarFrame, items=["/chatter", "/chatter2"], width=200
        )
        scrollableCheckBoxes.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="ns")

    def buildMainSection(self) -> None:
        """
        Build the response section frame with widgets
        The response section contain the server response and the directory list text boxes
        """
        mainSectionFrame = ctk.CTkFrame(self)
        mainSectionFrame.grid(row=0, column=1, sticky="nsew", padx=(5, 5), pady=(10, 10))
        mainSectionFrame.grid_columnconfigure((0, 2), weight=1)
        mainSectionFrame.grid_rowconfigure(5, weight=1)

        terminalResponseLabel = ctk.CTkLabel(mainSectionFrame, text="Server Response")
        terminalResponseLabel.grid(
            row=0, column=0, columnspan=5, padx=(10, 10), pady=(10, 10), sticky="wns"
        )
        terminalResponseTextbox = ctk.CTkTextbox(mainSectionFrame, width=250, height=250)
        terminalResponseTextbox.grid(
            row=1, column=0, columnspan=5, padx=(10, 10), pady=(10, 10), sticky="nsew"
        )
        terminalResponseTextbox.configure(state="disabled")
        self.responseWidgets["terminalResponseTextbox"] = terminalResponseTextbox

        mainEntry = ctk.CTkEntry(
            mainSectionFrame,
            placeholder_text="Prefix for bag name, final name will be {prefix}{timestamp}.bag",
        )
        mainEntry.grid(row=2, column=0, columnspan=3, padx=20, pady=(10, 0), sticky="nsew")

        startButton = ctk.CTkButton(mainSectionFrame, command=None, text="Start Recording")
        startButton.grid(row=2, column=3, padx=20, pady=10, sticky="nsew")

        stopButton = ctk.CTkButton(mainSectionFrame, command=None, text="Stop Recording")
        stopButton.grid(row=2, column=4, padx=20, pady=10, sticky="nsew")

        commandLabel = ctk.CTkLabel(mainSectionFrame, text="Generated rosbag command")
        commandLabel.grid(row=3, column=0, columnspan=5, padx=(10, 10), pady=(20, 20), sticky="wns")
        commandTextbox = ctk.CTkTextbox(mainSectionFrame, width=250, height=150)
        commandTextbox.grid(
            row=4, column=0, columnspan=5, padx=(10, 10), pady=(0, 20), sticky="nsew"
        )
        commandTextbox.configure(state="disabled")
        self.responseWidgets["commandTextbox"] = commandTextbox

    def buildOptionsSection(self) -> None:
        """
        build the options section frame for the rosbag command
        """

        optionFrame = ctk.CTkFrame(self, width=140)
        optionFrame.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="nwe")

        loginLabel = ctk.CTkLabel(master=optionFrame, text="Enter rosbag options")
        loginLabel.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="n")

        lengthEntry = ctk.CTkEntry(master=optionFrame, placeholder_text="length")
        lengthEntry.grid(row=1, column=2, padx=5, pady=5, sticky="n")

        limitEntry = ctk.CTkEntry(master=optionFrame, placeholder_text="limit")
        limitEntry.grid(row=2, column=2, padx=5, pady=10, sticky="n")

        timeEntry = ctk.CTkEntry(master=optionFrame, placeholder_text="time")
        timeEntry.grid(row=2, column=2, padx=5, pady=10, sticky="n")
