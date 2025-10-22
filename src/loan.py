"""
Loan module for library system.
"""
from datetime import datetime


class Loan:
    """
    Represents a loan of an item to a patron.
    """

    def __init__(self, item, due_date):
        """
        Initialize a Loan.

        Args:
            item: The BorrowableItem being loaned
            due_date: Date when the loan is due
        """
        self._item = item
        self._due_date = due_date

    def __str__(self):
        """String representation of the loan."""
        today = datetime.now().date()
        if self._due_date < today:
            days_overdue = (today - self._due_date).days
            return f"{self._item._name} (OVERDUE by {days_overdue} days)"
        return f"{self._item._name} (Due: {self._due_date})"
