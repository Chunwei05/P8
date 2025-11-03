"""
User interface module for the BAT system.
"""

from src import user_input
from src import search


class BatUI:
    """
    User interface for the Borrowing Administration Tool.
    """

    def __init__(self, data_manager, business_logic=None):
        """
        Initialize the UI.

        Args:
            data_manager: DataManager instance
            business_logic: BusinessLogic instance (optional)
        """
        self.data_manager = data_manager
        self.business_logic = business_logic

    def run(self):
        """Run the BAT system (alias for main_menu)."""
        self.main_menu()

    def main_menu(self):
        """Display and handle the main menu."""
        self.data_manager.load_data()

        while True:
            print("\n=== BAT Main Menu ===")
            print("1. Borrow item")
            print("2. Return item")
            print("3. Search patrons")
            print("4. View patron details")
            print("5. Pay fees")
            print("6. Exit")

            choice = user_input.get_menu_choice(
                "Enter choice: ",
                ['1', '2', '3', '4', '5', '6']
            )

            if choice == '1':
                self.borrow_item()
            elif choice == '2':
                self.return_item()
            elif choice == '3':
                self.search_patrons()
            elif choice == '4':
                self.view_patron_details()
            elif choice == '5':
                self.pay_fees()
            elif choice == '6':
                self.data_manager.save_data()
                print("Data saved. Goodbye!")
                break

    def search_patrons(self):
        """Handle patron search."""
        print("\n=== Search Patrons ===")
        print("1. Search by name")
        print("2. Search by ID")
        print("3. Search by age")
        print("4. Search by name and age")
        print("5. Back to main menu")

        choice = user_input.get_menu_choice(
            "Enter choice: ",
            ['1', '2', '3', '4', '5']
        )

        if choice == '1':
            self.search_by_name()
        elif choice == '2':
            self.search_by_id()
        elif choice == '3':
            self.search_by_age()
        elif choice == '4':
            self.search_by_name_and_age()

    def search_by_name(self):
        """Search for a patron by name."""
        name = user_input.get_string_input("Enter patron name: ")
        patron = search.search_patron_by_name(
            self.data_manager._patron_data,
            name
        )
        if patron:
            print(f"\nFound: {patron}")
        else:
            print(f"\nNo patron found with name: {name}")

    def search_by_id(self):
        """Search for a patron by ID."""
        patron_id = user_input.get_int_input("Enter patron ID: ")
        patron = search.search_patron_by_id(
            self.data_manager._patron_data,
            patron_id
        )
        if patron:
            print(f"\nFound: {patron}")
        else:
            print(f"\nNo patron found with ID: {patron_id}")

    def search_by_age(self):
        """Search for patrons by age."""
        age = user_input.get_int_input_in_range(
            "Enter age: ",
            0,
            120
        )
        patrons = search.search_patron_by_age(
            self.data_manager._patron_data,
            age
        )
        if patrons:
            print(f"\nFound {len(patrons)} patron(s):")
            for patron in patrons:
                print(f"  - {patron}")
        else:
            print(f"\nNo patrons found with age: {age}")

    def search_by_name_and_age(self):
        """Search for patrons by name and age."""
        name = user_input.get_string_input("Enter patron name: ")
        age = user_input.get_int_input_in_range(
            "Enter age: ",
            0,
            120
        )
        patrons = search.search_patron_by_name_and_age(
            self.data_manager._patron_data,
            name,
            age
        )
        if patrons:
            print(f"\nFound {len(patrons)} patron(s):")
            for patron in patrons:
                print(f"  - {patron}")
        else:
            print(
                f"\nNo patrons found with name "
                f"'{name}' and age {age}"
            )

    def borrow_item(self):
        """Handle borrowing an item."""
        print("\n=== Borrow Item ===")

        item_id = user_input.get_int_input("Enter item ID: ")
        item = search.search_item_by_id(
            self.data_manager._catalogue_data,
            item_id
        )

        if item is None:
            print(f"Item with ID {item_id} not found.")
            return

        print(f"Item: {item}")

        patron_id = user_input.get_int_input("Enter patron ID: ")
        patron = search.search_patron_by_id(
            self.data_manager._patron_data,
            patron_id
        )

        if patron is None:
            print(f"Patron with ID {patron_id} not found.")
            return

        result = self.business_logic.borrow_item(patron, item)

        if result is True:
            print("Success! Item borrowed.")
        else:
            print(f"Cannot borrow: {result}")

    def return_item(self):
        """Handle returning an item."""
        print("\n=== Return Item ===")

        patron_id = user_input.get_int_input("Enter patron ID: ")
        patron = search.search_patron_by_id(
            self.data_manager._patron_data,
            patron_id
        )

        if patron is None:
            print(f"Patron with ID {patron_id} not found.")
            return

        if not patron._loans:
            print("Patron has no items on loan.")
            return

        print("\nCurrent loans:")
        for loan in patron._loans:
            print(f"  - ID: {loan._item._id}, Item: {loan._item}")

        item_id = user_input.get_int_input(
            "Enter item ID to return: "
        )

        result = self.business_logic.return_item(patron, item_id)

        if result:
            print("Item returned successfully.")
        else:
            print("Patron does not have this item on loan.")

    def view_patron_details(self):
        """Display detailed information about a patron."""
        print("\n=== View Patron Details ===")

        patron_id = user_input.get_int_input("Enter patron ID: ")
        patron = search.search_patron_by_id(
            self.data_manager._patron_data,
            patron_id
        )

        if patron is None:
            print(f"Patron with ID {patron_id} not found.")
            return

        print("\n" + "=" * 50)
        print(patron.to_full_string())

        overdue_fees = patron.calculate_overdue_fees()
        if overdue_fees > 0:
            print(f"Overdue fees: ${overdue_fees:.2f}")

        print("=" * 50)

    def pay_fees(self):
        """Handle fee payment."""
        print("\n=== Pay Fees ===")

        patron_id = user_input.get_int_input("Enter patron ID: ")
        patron = search.search_patron_by_id(
            self.data_manager._patron_data,
            patron_id
        )

        if patron is None:
            print(f"Patron with ID {patron_id} not found.")
            return

        print(
            f"Outstanding fees: "
            f"${patron._outstanding_fees:.2f}"
        )

        if patron._outstanding_fees == 0:
            print("No fees to pay.")
            return

        amount = user_input.get_float_input_in_range(
            f"Enter amount to pay "
            f"(max ${patron._outstanding_fees:.2f}): ",
            0.01,
            patron._outstanding_fees
        )

        remaining = patron.pay_fee(amount)

        if remaining == 0:
            print("Payment successful! No outstanding fees.")
        else:
            print(
                f"Payment successful! "
                f"Remaining: ${remaining:.2f}"
            )
