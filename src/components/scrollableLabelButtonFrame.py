"""
Scrollable frame with labels and buttons for bag list
"""

from typing import Optional, Any, Union, Callable, Tuple, List, Dict
from tkinter import ttk

import os
import customtkinter as ctk

from PIL import Image
from ..constants import Constants


class ScrollableLabelButtonFrame(ctk.CTkScrollableFrame):  # type: ignore # pylint: disable=R0901
    """
    Scrollable frame with labels and buttons for bag list
    """

    def __init__(
        self,
        master: Union[ctk.CTk, ctk.CTkFrame],
        bagDescription: Dict[str, Any],
        playCommand: Callable[[str], Any],
        deleteCommand: Callable[[str], Any],
        **kwargs: Optional[Any],
    ) -> None:
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 3, 4), weight=0)
        self.grid_columnconfigure((2), weight=1)

        self.trashImage = ctk.CTkImage(
            light_image=Image.open(os.path.join(Constants.IMAGE_PATH, "trash_dark.png")),
            dark_image=Image.open(os.path.join(Constants.IMAGE_PATH, "trash_dark.png")),
            size=(20, 20),
        )

        self.playImage = ctk.CTkImage(
            light_image=Image.open(os.path.join(Constants.IMAGE_PATH, "play_dark.png")),
            dark_image=Image.open(os.path.join(Constants.IMAGE_PATH, "play_dark.png")),
            size=(20, 20),
        )

        self.playCommand = playCommand
        self.deleteCommand = deleteCommand
        self.labelsList: List[Tuple[ctk.CTkLabel, ctk.CTkLabel, ctk.CTkLabel]] = []
        self.buttonList: List[Tuple[ctk.CTkButton, ctk.CTkButton]] = []
        self.sepratorList: List[ttk.Separator] = []

        self.addItems(bagDescription)

    def addItem(self, key: str, item: str, timestamp: str, description: str) -> None:
        """
        Add a label and button to the frame
        """
        row = len(self.labelsList) * 2

        itemLabel = ctk.CTkLabel(self, text=item, padx=5, anchor="w", width=200)
        itemLabel.grid(row=row, column=0, padx=(0, 10), pady=(0, 10), sticky="w")

        timestampLabel = ctk.CTkLabel(self, text=timestamp, padx=5, anchor="w", width=100)
        timestampLabel.grid(row=row, column=1, padx=(0, 10), pady=(0, 10), sticky="w")

        descriptionLabel = ctk.CTkLabel(self, text=description, padx=5, anchor="w")
        descriptionLabel.grid(
            row=row,
            column=2,
            padx=(0, 10),
            pady=(0, 10),
            sticky="we",
        )

        deleteButton = ctk.CTkButton(self, text="", width=50, height=24, image=self.trashImage)
        deleteButton.configure(command=lambda: self.deleteCommand(key))
        deleteButton.grid(row=row, column=3, pady=(0, 10), padx=5)

        playButton = ctk.CTkButton(self, text="", width=50, height=24, image=self.playImage)
        playButton.configure(command=lambda: self.playCommand(key))
        playButton.grid(row=row, column=4, pady=(0, 10), padx=5)

        styl = ttk.Style()
        styl.configure("TSeparator", background="grey")

        separator = ttk.Separator(self, orient="horizontal", style="TSeparator")
        separator.grid(row=row + 1, column=0, columnspan=5, sticky="we", pady=(0, 5))

        self.labelsList.append((itemLabel, timestampLabel, descriptionLabel))
        self.buttonList.append((deleteButton, playButton))
        self.sepratorList.append(separator)

    def removeItem(self, item: str) -> None:
        """
        Remove a label and button from the frame
        """
        for labels, buttons, seprator in zip(self.labelsList, self.buttonList, self.sepratorList):
            if item == labels[0].cget("text"):
                for label in labels:
                    label.destroy()
                for button in buttons:
                    button.destroy()
                seprator.destroy()
                self.labelsList.remove(labels)
                self.buttonList.remove(buttons)
                self.sepratorList.remove(seprator)
                return

    def clear(self) -> None:
        """
        Clear the frame
        """

        for labels, buttons, seprator in zip(self.labelsList, self.buttonList, self.sepratorList):
            for label in labels:
                label.destroy()
            for button in buttons:
                button.destroy()
            seprator.destroy()
        self.labelsList.clear()
        self.buttonList.clear()
        self.sepratorList.clear()

    def addItems(self, items: Dict[str, Any]) -> None:
        """
        Add multiple items to the frame
        """
        for key, value in items.items():
            self.addItem(key, value["name"], value["date"], value["description"])
