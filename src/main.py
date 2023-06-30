"""
Main module of the application.
"""

from .view import RosBagClientGui
from .presenter import RosBagPresenter


def main() -> None:
    """
    Main function of the application.
    """
    view = RosBagClientGui()
    presenter = RosBagPresenter(view)
    presenter.run()
    view.mainloop()


if __name__ == "__main__":
    main()
