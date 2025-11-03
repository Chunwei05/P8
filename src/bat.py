"""
Main entry point for the BAT (Borrowing and Access Tracking) system.
"""
from src.bat_ui import BatUI
from src.business_logic import BusinessLogic
from src.data_mgmt import DataManager


def main():
    """
    Main function to run the BAT system.
    """
    data_manager = DataManager()
    business_logic = BusinessLogic()
    ui = BatUI(data_manager, business_logic)
    ui.run()


if __name__ == "__main__":
    main()
