"""
Record page
"""

from typing import Dict, Any, Union, Optional

import customtkinter as ctk

from .scrollableLabelButtonFrame import ScrollableLabelButtonFrame


class BagsListFrame(ctk.CTkFrame):  # type: ignore # pylint: disable=R0901
    """
    Record frame
    """

    def __init__(self, master: Union[ctk.CTk, ctk.CTkFrame], **kwargs: Optional[Any]) -> None:
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.responseWidgets: Dict[str, ctk.CTkTextbox] = {}

    def buildGUI(self) -> None:
        """
        Build the GUI, runs all the methods that build the GUI.
        """

        scrollableLabelButtonFrame = ScrollableLabelButtonFrame(self, lambda: None, lambda: None)
        scrollableLabelButtonFrame.grid(
            row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nswe"
        )
