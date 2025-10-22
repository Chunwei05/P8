"""
Main entry point for the BAT (Borrowing Administration Tool) system.
"""

from src.bat_ui import BatUi
from src.business_logic import BusinessLogic
from src.data_mgmt import DataManager


class BorrowingAdministrationTool:
    """
    Main application class for the BAT system.
    """
    # pylint: disable=too-few-public-methods
    # This is a main application class with a single run method

    def __init__(self):
        """Initialize the BAT system."""
        self.data_manager = DataManager()
        self.business_logic = BusinessLogic(self.data_manager)
        self.user_interface = BatUi(
            self.business_logic,
            self.data_manager
        )

    def run(self):
        """Run the main application loop."""
        self.user_interface.main_menu()


if __name__ == "__main__":
    bat = BorrowingAdministrationTool()
    bat.run()
