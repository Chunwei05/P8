'''
Author: Charlotte Pierce

Assignment code for FIT2107 Software Quality and Testing.
Not to be shared or distributed without permission.
'''

from src import user_input
from src import data_mgmt
from src import search
from src import business_logic as logic


class BatUI():
    '''
    This class manages the UI screens of BAT and the transitions between them.
    '''

    def __init__(self, data_manager):
        '''
        Create a new instance of the UI. The initial screen will be
        set to the main menu screen.

            Args:
                data_manager (DataManager): a data manager with patron
                    and catalogue data loaded.
        '''
        self._current_screen = self._main_menu
        self._data_manager = data_manager

    def get_current_screen(self):
        '''
        Retrieve the current menu screen.

            Returns:
                A string representation of the current menu screen. Possible values are
                "MAIN MENU", "LOAN ITEM", "RETURN ITEM", "SEARCH FOR PATRON", "REGISTER PATRON",
                "ACCESS MAKERSPACE", and "QUIT".
        '''
        match self._current_screen:
            case self._main_menu:
                return "MAIN MENU"
            case self._loan_item:
                return "LOAN ITEM"
            case self._return_item:
                return "RETURN ITEM"
            case self._search_for_patron:
                return "SEARCH FOR PATRON"
            case self._register_patron:
                return "REGISTER PATRON"
            case self._access_makerspace:
                return "ACCESS MAKERSPACE"
            case self._quit:
                return "QUIT"

    def run_current_screen(self):
        '''
        Run the current menu screen.
        '''
        return self._current_screen()

    def _main_menu(self):
        '''
        The main menu screen of BAT.
        '''
        print("\nMAIN MENU")
        print("=========")
        print("What would you like to do?")
        print("1. Loan an item")
        print("2. Return an item")
        print("3. Search for a patron")
        print("4. Register a new patron")
        print("5. Access makerspace")
        print("6. Quit")

        user_choice = user_input.get_int_input(1, 6)

        match user_choice:
            case 1:
                self._current_screen = self._loan_item
            case 2:
                self._current_screen = self._return_item
            case 3:
                self._current_screen = self._search_for_patron
            case 4:
                self._current_screen = self._register_patron
            case 5:
                self._current_screen = self._access_makerspace
            case 6:
                self._current_screen = self._quit

        return self._current_screen

    def _loan_item(self):
        '''
        The loan item screen of BAT.
        '''
        print("\nLOAN ITEM")
        print("=========")

        patron_id = user_input.get_int_input(0, 999999999, "Enter patron ID: ")
        patron = self._data_manager.get_patron_by_id(patron_id)

        if patron is None:
            print("Patron not found.")
            self._current_screen = self._main_menu
        else:
            print(f"Patron found: {patron._name}")

            print("\nAvailable items to loan:")
            print("1. Book")
            print("2. Gardening tool")
            print("3. Carpentry tool")

            item_type = user_input.get_int_input(1, 3)

            print("\nAvailable items:")
            catalogue = self._data_manager.get_catalogue()
            for item in catalogue:
                if item._type == item_type:
                    print(f"{item._id}: {item._name} ({item._year})")

            item_id = user_input.get_int_input(0, 999999999, "Enter item ID: ")
            item = self._data_manager.get_item_by_id(item_id)

            if item is None:
                print("Item not found.")
            else:
                loan_allowed = logic.check_loan_allowed(patron, item)

                if loan_allowed is True:
                    print(f"\nLoan of {item._name} to {patron._name} approved.")
                    self._data_manager.create_loan(patron_id, item_id)
                else:
                    print(f"\nLoan of {item._name} to {patron._name} denied.")
                    print("Reason: " + loan_allowed)

            self._current_screen = self._main_menu

        return self._current_screen

    def _return_item(self):
        '''
        The return item screen of BAT.
        '''
        print("\nRETURN ITEM")
        print("===========")

        patron_id = user_input.get_int_input(0, 999999999, "Enter patron ID: ")
        patron = self._data_manager.get_patron_by_id(patron_id)

        if patron is None:
            print("Patron not found.")
            self._current_screen = self._main_menu
        else:
            print(f"Patron found: {patron._name}")

            loans = patron._loans
            if not loans:
                print("No items currently on loan.")
            else:
                print("\nItems currently on loan:")
                for loan in loans:
                    print(f"{loan._id}: {loan._item._name}")

                loan_id = user_input.get_int_input(0, 999999999, "Enter loan ID: ")
                loan = self._data_manager.get_loan_by_id(loan_id)

                if loan is None:
                    print("Loan not found.")
                else:
                    print(f"\nReturn of {loan._item._name} by {patron._name} processed.")
                    self._data_manager.return_loan(loan_id)

            self._current_screen = self._main_menu

        return self._current_screen

    def _search_for_patron(self):
        '''
        The search for patron screen of BAT.
        '''
        print("\nSEARCH FOR PATRON")
        print("=================")

        print("How would you like to search?")
        print("1. By name")
        print("2. By age")

        search_choice = user_input.get_int_input(1, 2)

        match search_choice:
            case 1:
                search_term = user_input.get_string_input("Enter name to search for: ")
                results = search.search_patrons_by_name(self._data_manager.get_patrons(), search_term)
            case 2:
                search_term = user_input.get_int_input(0, 150, "Enter age to search for: ")
                results = search.search_patrons_by_age(self._data_manager.get_patrons(), search_term)

        if not results:
            print("No matching patrons found.")
        else:
            print("\nMatching patrons:")
            for patron in results:
                print(f"{patron._id}: {patron._name}, age {patron._age}")

        input("\nPress enter to continue...")

        self._current_screen = self._main_menu
        return self._current_screen

    def _register_patron(self):
        '''
        The register patron screen of BAT.
        '''
        print("\nREGISTER PATRON")
        print("===============")

        print("Enter patron details:")
        name = user_input.get_string_input("Name: ")
        age = user_input.get_int_input(0, 150, "Age: ")

        patron = self._data_manager.create_patron(name, age)
        print(f"\nPatron {patron._name} registered with ID {patron._id}.")

        input("\nPress enter to continue...")

        self._current_screen = self._main_menu
        return self._current_screen

    def _access_makerspace(self):
        '''
        The access makerspace screen of BAT.
        '''
        print("\nACCESS MAKERSPACE")
        print("=================")

        patron_id = user_input.get_int_input(0, 999999999, "Enter patron ID: ")
        patron = self._data_manager.get_patron_by_id(patron_id)

        if patron is None:
            print("Patron not found.")
            self._current_screen = self._main_menu
        else:
            print(f"Patron found: {patron._name}")

            access_allowed = logic.check_makerspace_access(patron)

            if access_allowed is True:
                print(f"\n{patron._name} is allowed to access the makerspace.")
            else:
                print(f"\n{patron._name} is not allowed to access the makerspace.")
                print("Reason: " + access_allowed)

            input("\nPress enter to continue...")

            self._current_screen = self._main_menu

        return self._current_screen

    def _quit(self):
        '''
        The quit menu screen of BAT. Saves the current state of patron and
        catalogue data, overriting any existing data files.
        '''
        print("Bye...")
        self._data_manager.save_patrons()
        self._data_manager.save_catalogue()

        return self._quit