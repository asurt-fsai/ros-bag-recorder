"""
ROSBAG GUI
"""

from typing import Dict, Protocol, Optional

import os
import tkinter as tk
import customtkinter as ctk

from PIL import Image
from .pages.bagListFrame.bagsListView import BagsListFrame
from .pages.recordFrame.recordView import RecordView
from .constants import Constants, Pages


class RosBagPresenter(Protocol):
    """
    Record Presenter protocol
    """

    # pylint: disable=C0116

    def handleRecordButtonEvent(self, event: Optional[tk.EventType] = None) -> None:
        ...

    def handleAvailableBagsButtonEvent(self, event: Optional[tk.EventType] = None) -> None:
        ...


class RosBagClientGui(ctk.CTk):  # type: ignore # pylint: disable=R0901
    """
    RosBag Client Gui
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("RosBag Client")
        self.geometry(f"{1600}x{900}")
        icon = tk.PhotoImage(file=f"{os.path.realpath(os.path.dirname(__file__))}/../favicon.png")
        self.tk.call("wm", "iconphoto", self._w, icon)

        self.buttonWidgets: Dict[str, ctk.CTkEntry] = {}
        self.pages: Dict[Pages, ctk.CTkFrame] = {}

    def buildGUI(self, presenter: RosBagPresenter) -> Dict[Pages, ctk.CTkFrame]:
        """
        Build the GUI, runs all the methods that build the GUI.
        """

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buildSidebar(presenter)

        self.pages[Pages.RECORD] = RecordView(self, fg_color="transparent")
        self.pages[Pages.RECORD].grid(row=0, column=1, sticky="nsew")

        self.pages[Pages.AVAILABLE_BAGS] = BagsListFrame(self, fg_color="transparent")

        return self.pages

    def buildSidebar(self, presenter: RosBagPresenter) -> None:
        """
        Build the sidebar frame with widgets
        The sidebar contain the name of the application and the appearance mode option menu
        """

        ### SIDEBAR MAIN FRAME ###
        sideBarFrame = ctk.CTkFrame(self, width=140, corner_radius=0)
        sideBarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        sideBarFrame.grid_rowconfigure(4, weight=1)

        ### SIDEBAR LABEL ###
        nameLabel = ctk.CTkLabel(
            sideBarFrame,
            text="Rosbag\nClient",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        nameLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        ### SIDEBAR Buttons ###
        recordImage = ctk.CTkImage(
            light_image=Image.open(os.path.join(Constants.IMAGE_PATH, "record_light.png")),
            dark_image=Image.open(os.path.join(Constants.IMAGE_PATH, "record_dark.png")),
            size=(20, 20),
        )

        playImage = ctk.CTkImage(
            light_image=Image.open(os.path.join(Constants.IMAGE_PATH, "play_light.png")),
            dark_image=Image.open(os.path.join(Constants.IMAGE_PATH, "play_dark.png")),
            size=(20, 20),
        )

        recordButton = ctk.CTkButton(
            sideBarFrame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Record",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=recordImage,
            anchor="w",
            command=presenter.handleRecordButtonEvent,
        )
        recordButton.grid(row=1, column=0, sticky="ew")
        self.buttonWidgets["recordButton"] = recordButton

        availableBagsbutton = ctk.CTkButton(
            sideBarFrame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Available Bags",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=playImage,
            anchor="w",
            command=presenter.handleAvailableBagsButtonEvent,
        )
        availableBagsbutton.grid(row=2, column=0, sticky="ew")
        self.buttonWidgets["availableBagsbutton"] = availableBagsbutton

        ### SIDEBAR APPEARANCE MODE ###
        appearanceModeLabel = ctk.CTkLabel(sideBarFrame, text="Appearance Mode:", anchor="w")
        appearanceModeLabel.grid(row=5, column=0, padx=20, pady=(10, 0))
        appearanceModeOptioneMenu = ctk.CTkOptionMenu(
            sideBarFrame,
            values=["Light", "Dark", "System"],
            command=self._changeAppearanceModeEvent,
        )
        appearanceModeOptioneMenu.grid(row=6, column=0, padx=20, pady=(10, 30))

        appearanceModeOptioneMenu.set("Dark")

    def selectPage(self, name: Pages) -> None:
        """
        Select a frame to be displayed in the main area of the application
        """

        self.buttonWidgets["recordButton"].configure(
            fg_color=("gray75", "gray25") if name == Pages.RECORD else "transparent"
        )
        self.buttonWidgets["availableBagsbutton"].configure(
            fg_color=("gray75", "gray25") if name == Pages.AVAILABLE_BAGS else "transparent"
        )

        if name == Pages.RECORD:
            self.pages[Pages.RECORD].grid(row=0, column=1, sticky="nsew")
        else:
            self.pages[Pages.RECORD].grid_forget()

        if name == Pages.AVAILABLE_BAGS:
            self.pages[Pages.AVAILABLE_BAGS].grid(row=0, column=1, sticky="nsew")
        else:
            self.pages[Pages.AVAILABLE_BAGS].grid_forget()

    def _changeAppearanceModeEvent(self, appearanceMode: str) -> None:
        """
        Change the appearance mode of the application

        parameters
        ----------
        appearanceMode: str
            The appearance mode to change to (Dark/Light/System)
        """
        ctk.set_appearance_mode(appearanceMode)
