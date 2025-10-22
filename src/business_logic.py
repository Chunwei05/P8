"""
Business logic for the library system.
"""
from src.borrowable_item import BorrowableItem
from src.loan import Loan


class BusinessLogic:
    """
    Handles business rules and validation for library operations.
    """

    @staticmethod
    def check_loan_allowed(patron, item):
        """
        Check if a patron is allowed to borrow an item.

        Args:
            patron: The Patron object attempting to borrow
            item: The BorrowableItem to be borrowed

        Returns:
            tuple: (bool, str) - (allowed, reason_if_not_allowed)
        """
        # Check if item is available
        if not isinstance(item, BorrowableItem):
            return False, "Invalid item"

        if item._on_loan >= item._num_copies:
            return False, "No copies available"

        # Check patron loan limit
        patron_type = patron.get_type()
        max_loans = {"Minor": 3, "Regular": 5, "Elderly": 10}

        if len(patron._loans) >= max_loans.get(patron_type, 5):
            return False, f"Loan limit reached for {patron_type}"

        # Check outstanding fees
        if patron._outstanding_fees > 0:
            return False, "Outstanding fees must be paid"

        # Check age restrictions
        item_type = item._type
        if item_type == "Reference Book":
            return False, "Reference books cannot be borrowed"

        if patron._age < 18:
            if item_type in ["Gardening Tool", "Carpentry Tool"]:
                return False, "Minors cannot borrow tools"

        # Check training requirements
        if item_type == "Gardening Tool" and not patron._gardening_tool_training:
            return False, "Gardening tool training required"

        if item_type == "Carpentry Tool" and not patron._carpentry_tool_training:
            return False, "Carpentry tool training required"

        # Check for duplicate loans
        for loan in patron._loans:
            if loan._item._type == item_type:
                return False, f"Already have a {item_type} on loan"

        # Check specific item restrictions
        if item_type in ["Laptop", "Study Room"]:
            loan_period = BusinessLogic._get_loan_period(item_type)
            if loan_period == 0:
                return False, f"{item_type} cannot be borrowed"

        return True, "Loan allowed"

    @staticmethod
    def _get_loan_period(item_type):
        """
        Get the loan period for an item type.

        Args:
            item_type: Type of the item

        Returns:
            int: Number of days for loan period
        """
        loan_periods = {
            "Fiction Book": 21,
            "Non-Fiction Book": 21,
            "Magazine": 7,
            "DVD": 7,
            "Laptop": 3,
            "Study Room": 1,
            "Gardening Tool": 14,
            "Carpentry Tool": 14,
        }
        return loan_periods.get(item_type, 14)

    @staticmethod
    def process_loan(patron, item):
        """
        Process a loan transaction.

        Args:
            patron: The Patron borrowing the item
            item: The BorrowableItem being borrowed

        Returns:
            tuple: (bool, str) - (success, message)
        """
        allowed, reason = BusinessLogic.check_loan_allowed(patron, item)
        if not allowed:
            return False, reason

        loan_period = BusinessLogic._get_loan_period(item._type)
        patron.add_loan(item, loan_period)
        return True, f"Loan successful. Due in {loan_period} days."

    @staticmethod
    def check_return_allowed(patron, item_id):
        """
        Check if a patron can return an item.

        Args:
            patron: The Patron returning the item
            item_id: ID of the item being returned

        Returns:
            tuple: (bool, str) - (allowed, reason_if_not_allowed)
        """
        if not patron.has_item(item_id):
            return False, "Item not on loan to this patron"

        return True, "Return allowed"

    @staticmethod
    def process_return(patron, item_id):
        """
        Process a return transaction.

        Args:
            patron: The Patron returning the item
            item_id: ID of the item being returned

        Returns:
            tuple: (bool, str, float) - (success, message, fees)
        """
        allowed, reason = BusinessLogic.check_return_allowed(patron, item_id)
        if not allowed:
            return False, reason, 0.0

        # Calculate overdue fees before return
        overdue_fees = patron.calculate_overdue_fees()

        # Process return
        success = patron.return_item(item_id)
        if success:
            if overdue_fees > 0:
                patron.add_fee(overdue_fees)
                return True, f"Return successful. Overdue fee: ${overdue_fees:.2f}", overdue_fees
            return True, "Return successful. No fees.", 0.0

        return False, "Return failed", 0.0

    @staticmethod
    def check_makerspace_access(patron):
        """
        Check if a patron can access the makerspace.

        Args:
            patron: The Patron requesting access

        Returns:
            tuple: (bool, str) - (allowed, reason_if_not_allowed)
        """
        # Check age requirement
        if patron._age < 18:
            return False, "Must be 18 or older to access makerspace"

        # Check training requirement
        if not patron._makerspace_training:
            return False, "Makerspace training required"

        return True, "Access granted"
