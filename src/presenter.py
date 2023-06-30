"""
Bag List Presenter
"""
from __future__ import annotations
from typing import Protocol, Optional, Dict

import tkinter as tk
import customtkinter as ctk

from .constants import Pages
from .logic.fileSystemInterface import FileSystemInterface
from .pages.recordFrame.recordPresenter import RecordPresenter
from .pages.bagListFrame.bagListPresenter import BagListPresenter


class RosBagClientGui(Protocol):  # pylint: disable=R0903
    """
    View Protocol
    """

    # pylint: disable=C0116

    def buildGUI(self, presenter: RosBagPresenter) -> Dict[Pages, ctk.CTkFrame]:
        ...

    def selectPage(self, name: Pages) -> None:
        ...


class RosBagPresenter:
    """
    Bag List Presenter
    """

    # pylint: disable=W0613

    def __init__(self, view: RosBagClientGui) -> None:
        self.view = view
        self.recordPresenter: Optional[RecordPresenter] = None
        self.bagListPresenter: Optional[BagListPresenter] = None

    def handleRecordButtonEvent(self, event: Optional[tk.EventType] = None) -> None:
        """
        Handle the record button event.
        """
        if not self.recordPresenter:
            return

        self.view.selectPage(Pages.RECORD)

    def handleAvailableBagsButtonEvent(self, event: Optional[tk.EventType] = None) -> None:
        """
        Handle the available bags button event.
        """
        if not self.bagListPresenter:
            return

        self.view.selectPage(Pages.AVAILABLE_BAGS)
        self.bagListPresenter.handleRefreshBags()

    def run(self) -> None:
        """
        Run the GUI.
        """
        pages = self.view.buildGUI(self)
        fileSystem = FileSystemInterface()

        self.recordPresenter = RecordPresenter(pages[Pages.RECORD])
        self.bagListPresenter = BagListPresenter(pages[Pages.AVAILABLE_BAGS], fileSystem)

        self.recordPresenter.run()
        self.bagListPresenter.run()
