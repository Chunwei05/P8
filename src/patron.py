"""
Module for Patron class and related functionality.
"""

from datetime import datetime, timedelta
from src.loan import Loan
from src import search


class Patron:
    """
    Represents a library patron.
    """
    # pylint: disable=too-many-instance-attributes
    # Eight attributes are necessary for patron management

    def __init__(self, patron_id, name, age, outstanding_fees=0.0,
                 gardening_tool_training=False,
                 carpentry_tool_training=False,
                 makerspace_training=False):
        """
        Initialize a Patron.

        Args:
            patron_id: Unique identifier for the patron
            name: Patron's name
            age: Patron's age
            outstanding_fees: Amount of fees owed
            gardening_tool_training: Whether patron has gardening training
            carpentry_tool_training: Whether patron has carpentry training
            makerspace_training: Whether patron has makerspace training
        """
        self._id = patron_id
        self._name = name
        self._age = age
        self._outstanding_fees = outstanding_fees
        self._gardening_tool_training = gardening_tool_training
        self._carpentry_tool_training = carpentry_tool_training
        self._makerspace_training = makerspace_training
        self._loans = []

    def get_type(self):
        """
        Determine the patron type based on age.

        Returns:
            String representing patron type
        """
        if self._age < 18:
            return "Minor"
        if self._age >= 65:
            return "Elderly"
        return "Regular"

    def add_loan(self, item, due_days=14):
        """
        Add a loan to the patron's record.

        Args:
            item: The BorrowableItem being loaned
            due_days: Number of days until due (default 14)
        """
        due_date = datetime.now().date() + timedelta(days=due_days)
        loan = Loan(item, due_date)
        self._loans.append(loan)
        item._on_loan += 1

    def return_item(self, item_id):
        """
        Return an item and remove it from loans.

        Args:
            item_id: ID of the item being returned

        Returns:
            True if item was found and returned, False otherwise
        """
        for loan in self._loans:
            if loan._item._id == item_id:
                self._loans.remove(loan)
                loan._item._on_loan -= 1
                return True
        return False

    def has_item(self, patron_id):
        """
        Check if patron has a specific item on loan.

        Args:
            patron_id: ID to check (note: parameter name should be item_id)

        Returns:
            True if patron has the item, False otherwise
        """
        for loan in self._loans:
            if loan._item._id == patron_id:
                return True
        return False

    def calculate_overdue_fees(self):
        """
        Calculate total overdue fees for all loans.

        Returns:
            Total overdue fees as float
        """
        total_fees = 0.0
        today = datetime.now().date()

        for loan in self._loans:
            if loan._due_date < today:
                days_overdue = (today - loan._due_date).days
                total_fees += days_overdue * 1.0

        return total_fees

    def add_fee(self, amount):
        """
        Add a fee to the patron's outstanding fees.

        Args:
            amount: Fee amount to add
        """
        self._outstanding_fees += amount

    def pay_fee(self, amount):
        """
        Pay off some or all outstanding fees.

        Args:
            amount: Amount to pay

        Returns:
            Remaining balance after payment
        """
        self._outstanding_fees -= amount
        if self._outstanding_fees < 0:
            self._outstanding_fees = 0
        return self._outstanding_fees

    def __str__(self):
        """String representation of the patron."""
        loan_count = len(self._loans)
        return (
            f"{self._name} (ID: {self._id}, Age: {self._age}, "
            f"Loans: {loan_count}, Fees: ${self._outstanding_fees:.2f})"
        )

    def to_full_string(self):
        """
        Full string representation including all loans.

        Returns:
            Detailed string with patron info and loans
        """
        result = str(self) + "\n"
        if self._loans:
            result += "  Current loans:\n"
            for loan in self._loans:
                result += f"    - {loan}\n"
        else:
            result += "  No current loans\n"
        return result
