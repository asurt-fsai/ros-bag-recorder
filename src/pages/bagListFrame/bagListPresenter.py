"""
Bag List Presenter
"""
from __future__ import annotations
from typing import Dict, Any, Protocol, Optional

import os
import tkinter as tk
from ...constants import Constants
from ...logic.fileSystemInterface import FileSystemInterface


class BagListView(Protocol):  # pylint: disable=R0903
    """
    View Protocol
    """

    # pylint: disable=C0116

    def buildGUI(self, presenter: BagListPresenter, bagsDescription: Dict[str, Any]) -> None:
        ...

    def clearBagList(self) -> None:
        ...

    def addBags(self, bagsDescription: Dict[str, Any]) -> None:
        ...


class BagListPresenter:
    """
    Bag List Presenter
    """

    # pylint: disable=W0613

    def __init__(self, view: BagListView, model: FileSystemInterface) -> None:
        self.view = view
        self.model = model

    def handlePlayBag(self, name: str, event: Optional[tk.EventType] = None) -> None:
        """
        handle start record the ros bag
        """
        os.system(
            f"gnome-terminal -e 'bash -c \
              \"rosbag play {os.path.join(Constants.BAG_DIR_PATH, name)}; exec bash\"'"
        )

    def handleDeleteBag(self, name: str, event: Optional[tk.EventType] = None) -> None:
        """
        handle delete the ros bag
        """
        self.model.removeBag(name)
        self.handleRefreshBags()

    def handleRefreshBags(self, event: Optional[tk.EventType] = None) -> None:
        """
        handle refresh the ros bags
        """

        self.model.loadDescriptionJson()
        self.view.clearBagList()
        self.view.addBags(self.model.bagDescription)

    def run(self) -> None:
        """
        Run the GUI.
        """

        self.view.buildGUI(self, {})
        self.handleRefreshBags()
