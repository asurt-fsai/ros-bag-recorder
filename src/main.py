"""
Main module of the application.
"""

from .view import RosBagClientGui


def main() -> None:
    """
    Main function of the application.
    """
    view = RosBagClientGui()
    view.buildGUI()
    view.mainloop()


if __name__ == "__main__":
    main()
