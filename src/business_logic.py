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


# Standalone functions for testing (wrapper functions around business logic)

def type_of_patron(age):
    """
    Determine patron type based on age.

    Args:
        age: Patron's age

    Returns:
        str: Patron type ("ERROR", "Minor", "Adult", or "Elderly")
    """
    if age < 0:
        return "ERROR"
    if age < 18:
        return "Minor"
    if age >= 90:
        return "Elderly"
    return "Adult"


def calculate_discount(age):
    """
    Calculate discount percentage based on age.

    Args:
        age: Patron's age

    Returns:
        str or float: "ERROR" for negative age, discount percentage (0-100) otherwise
    """
    if age < 0:
        return "ERROR"
    if age >= 90:
        return 100.0
    if age >= 65:
        return 15.0
    if age >= 50:
        return 10.0
    return 0.0


def can_borrow(item_type, patron_age, membership_length, fees_owed,
               gardening_tool_training, carpentry_tool_training):
    """
    Route to appropriate borrowing function based on item type.

    Args:
        item_type: Type of item to borrow
        patron_age: Patron's age
        membership_length: Days of membership
        fees_owed: Outstanding fees
        gardening_tool_training: Whether patron has gardening training
        carpentry_tool_training: Whether patron has carpentry training

    Returns:
        bool: True if patron can borrow the item
    """
    item_type_lower = item_type.lower()

    if item_type_lower == "book":
        return can_borrow_book(patron_age, membership_length, fees_owed)
    if item_type_lower == "gardening tool":
        return can_borrow_gardening_tool(patron_age, membership_length,
                                          fees_owed, gardening_tool_training)
    if item_type_lower == "carpentry tool":
        return can_borrow_carpentry_tool(patron_age, membership_length,
                                          fees_owed, carpentry_tool_training)

    # Unknown item types return False
    return False


def can_borrow_book(patron_age, membership_length, fees_owed):
    """
    Check if a patron can borrow a book.

    Args:
        patron_age: Patron's age
        membership_length: Days of membership
        fees_owed: Outstanding fees

    Returns:
        bool: True if patron can borrow a book
    """
    if membership_length >= 56:
        return False
    discount = calculate_discount(patron_age)
    if discount == "ERROR":
        return False
    discounted_fees = fees_owed * (1 - discount / 100)
    return discounted_fees <= 0


def can_borrow_gardening_tool(patron_age, membership_length, fees_owed,
                               gardening_tool_training):
    """
    Check if a patron can borrow a gardening tool.

    Args:
        patron_age: Patron's age
        membership_length: Days of membership
        fees_owed: Outstanding fees
        gardening_tool_training: Whether patron has training

    Returns:
        bool: True if patron can borrow a gardening tool
    """
    if not gardening_tool_training:
        return False
    if membership_length > 28:
        return False
    discount = calculate_discount(patron_age)
    if discount == "ERROR":
        return False
    discounted_fees = fees_owed * (1 - discount / 100)
    return discounted_fees <= 0


def can_borrow_carpentry_tool(patron_age, membership_length, fees_owed,
                               carpentry_tool_training):
    """
    Check if a patron can borrow a carpentry tool.

    Args:
        patron_age: Patron's age
        membership_length: Days of membership
        fees_owed: Outstanding fees
        carpentry_tool_training: Whether patron has training

    Returns:
        bool: True if patron can borrow a carpentry tool
    """
    if not carpentry_tool_training:
        return False
    if membership_length > 14:
        return False

    # Complex condition: fees_owed > 0 OR patron_age <= 18 OR patron_age >= 90
    if fees_owed > 0 or patron_age <= 18 or patron_age >= 90:
        return False

    return True


def can_use_makerspace(patron_age, outstanding_fees, makerspace_training):
    """
    Check if a patron can use the makerspace.

    Args:
        patron_age: Patron's age
        outstanding_fees: Outstanding fees
        makerspace_training: Whether patron has makerspace training

    Returns:
        bool: True if patron can use makerspace
    """
    patron_type = type_of_patron(patron_age)

    # Error or non-adult patrons cannot use makerspace
    if patron_type == "ERROR":
        return False
    if patron_type in ["Minor", "Elderly"]:
        return False

    # Must have training
    if not makerspace_training:
        return False

    # Check fees after discount
    discount = calculate_discount(patron_age)
    discounted_fees = outstanding_fees * (1 - discount / 100)

    if discounted_fees > 0:
        return False

    return True
