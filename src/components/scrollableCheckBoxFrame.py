"""
Scrollable frame with checkboxes for topic list
"""

from typing import List, Optional, Any, Union

import tkinter as tk
import customtkinter as ctk


class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):  # type: ignore # pylint: disable=R0901
    """
    Scrollable frame with checkboxes for topic list
    """

    def __init__(
        self,
        master: Union[ctk.CTk, ctk.CTkFrame],
        items: List[str],
        command: Optional[tk.EventType] = None,
        **kwargs: Optional[Any],
    ) -> None:
        super().__init__(master, **kwargs)

        self.command = command
        self.checkboxList: List[ctk.CTkCheckBox] = []
        for _, item in enumerate(items):
            self.addItem(item)

    def addItem(self, item: str) -> None:
        """
        Add a checkbox to the frame
        """

        checkbox = ctk.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkboxList), column=0, pady=(0, 10))
        self.checkboxList.append(checkbox)

    def removeItem(self, item: str) -> None:
        """
        Remove a checkbox from the frame
        """
        for checkbox in self.checkboxList:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkboxList.remove(checkbox)
                return

    def getCheckedItems(self) -> List[str]:
        """
        Get the checked items from the frame
        """
        return [checkbox.cget("text") for checkbox in self.checkboxList if checkbox.get() == 1]
