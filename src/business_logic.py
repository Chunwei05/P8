"""
Business logic for the BAT system.
"""

from datetime import datetime


def determine_loan_period(patron_type):
    """
    Determine loan period based on patron type.

    Args:
        patron_type: Type of patron (Minor, Elderly, Regular)

    Returns:
        Number of days for the loan period
    """
    if patron_type == "Minor":
        return 7
    if patron_type == "Elderly":
        return 21
    return 14


def calculate_item_loan_limit(
    patron_type,
    item_type,
    patron_age,
    has_gardening_training,
    has_carpentry_training,
    has_makerspace_training
):
    """
    Calculate maximum loan limit for an item type.

    Args:
        patron_type: Type of patron
        item_type: Type of item
        patron_age: Age of patron
        has_gardening_training: Whether patron has gardening training
        has_carpentry_training: Whether patron has carpentry training
        has_makerspace_training: Whether patron has makerspace training

    Returns:
        Maximum number of items that can be borrowed
    """
    # pylint: disable=too-many-arguments
    # All parameters are necessary for business logic
    if item_type in ["Book", "DVD", "Magazine"]:
        if patron_type == "Minor":
            return 2
        if patron_type == "Elderly":
            return 3
        return 4

    if item_type == "Gardening Tool":
        if patron_age < 16 or not has_gardening_training:
            return 0
        return 1

    if item_type == "Carpentry Tool":
        if patron_age < 16 or not has_carpentry_training:
            return 0
        return 1

    if item_type == "Makerspace Tool":
        if patron_age < 12 or not has_makerspace_training:
            return 0
        return 1

    return 0


class BusinessLogic:
    """
    Contains business logic for the BAT system.
    """

    def __init__(self, data_manager):
        """
        Initialize business logic.

        Args:
            data_manager: DataManager instance
        """
        self.data_manager = data_manager

    def borrow_item(self, patron, item):
        """
        Process borrowing an item.

        Args:
            patron: Patron object
            item: BorrowableItem object

        Returns:
            True if successful, error message string otherwise
        """
        if not item.available:
            return "Item not available"

        if len(patron._loans) >= 4:
            return "Patron has reached maximum loan limit"

        if patron._outstanding_fees > 0:
            return "Patron has outstanding fees"

        patron_type = patron.get_type()
        item_limit = calculate_item_loan_limit(
            patron_type,
            item._type,
            patron._age,
            patron._gardening_tool_training,
            patron._carpentry_tool_training,
            patron._makerspace_training
        )

        if item_limit == 0:
            return (
                "Patron not authorized to borrow this item type"
            )

        current_count = sum(
            1 for loan in patron._loans
            if loan._item._type == item._type
        )

        if current_count >= item_limit:
            return (
                f"Patron has reached limit for {item._type}"
            )

        loan_period = determine_loan_period(patron_type)
        patron.add_loan(item, loan_period)
        return True

    def return_item(self, patron, item_id):
        """
        Process returning an item.

        Args:
            patron: Patron object
            item_id: ID of item to return

        Returns:
            True if successful, False otherwise
        """
        result = patron.return_item(item_id)

        if result:
            overdue_fees = patron.calculate_overdue_fees()
            if overdue_fees > 0:
                patron.add_fee(overdue_fees)

        return result

    def check_loan_allowed(self, patron, item):
        """
        Check if a patron can borrow an item.

        Args:
            patron: Patron object
            item: BorrowableItem object

        Returns:
            Tuple of (bool, str) - (allowed, reason)
        """
        if not item.available:
            return False, "Item not available"

        if len(patron._loans) >= 4:
            return False, "Maximum loan limit reached"

        if patron._outstanding_fees > 0:
            return False, "Outstanding fees must be paid"

        patron_type = patron.get_type()
        item_limit = calculate_item_loan_limit(
            patron_type,
            item._type,
            patron._age,
            patron._gardening_tool_training,
            patron._carpentry_tool_training,
            patron._makerspace_training
        )

        if item_limit == 0:
            return False, "Not authorized for this item type"

        current_count = sum(
            1 for loan in patron._loans
            if loan._item._type == item._type
        )

        if current_count >= item_limit:
            return False, f"Limit reached for {item._type}"

        return True, "Loan allowed"

    def check_makerspace_access(self, patron):
        """
        Check if patron has makerspace access.

        Args:
            patron: Patron object

        Returns:
            bool: True if patron has access
        """
        if patron._age < 12:
            return False
        return patron._makerspace_training
