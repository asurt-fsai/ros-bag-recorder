"""
Record page
"""

from typing import Dict, Any, Union, Optional, Protocol


import tkinter as tk
import customtkinter as ctk
from ...components.scrollableLabelButtonFrame import ScrollableLabelButtonFrame


class BagListPresenter(Protocol):
    """
    Record Presenter protocol
    """

    # pylint: disable=C0116

    def handlePlayBag(self, name: str, event: Optional[tk.EventType] = None) -> None:
        ...

    def handleDeleteBag(self, name: str, event: Optional[tk.EventType] = None) -> None:
        ...


class BagsListFrame(ctk.CTkFrame):  # type: ignore # pylint: disable=R0901
    """
    Record frame
    """

    def __init__(self, master: Union[ctk.CTk, ctk.CTkFrame], **kwargs: Optional[Any]) -> None:
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.widgets: Dict[str, ctk.CTkBaseClass] = {}

    def buildGUI(self, presenter: BagListPresenter, bagDescription: Dict[str, Any]) -> None:
        """
        Build the GUI, runs all the methods that build the GUI.
        """

        scrollableLabelButtonFrame = ScrollableLabelButtonFrame(
            self, bagDescription, presenter.handlePlayBag, presenter.handleDeleteBag
        )
        scrollableLabelButtonFrame.grid(
            row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nswe"
        )
        self.widgets["scrollableLabelButtonFrame"] = scrollableLabelButtonFrame

    def clearBagList(self) -> None:
        """
        Clear the bag list
        """
        self.widgets["scrollableLabelButtonFrame"].clear()

    def addBags(self, bagsDescription: Dict[str, Any]) -> None:
        """
        Add bags to the bag list
        """
        self.widgets["scrollableLabelButtonFrame"].addItems(bagsDescription)
