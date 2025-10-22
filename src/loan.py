"""
Module for Loan class.
"""

from datetime import datetime, timedelta


class Loan:
    """
    Represents a loan of an item to a patron.
    """

    def __init__(self, item, due_date):
        """
        Initialize a Loan.

        Args:
            item: The BorrowableItem being loaned
            due_date: The date the item is due to be returned
        """
        self._item = item
        if isinstance(due_date, str):
            self._due_date = datetime.strptime(
                due_date, "%Y-%m-%d"
            ).date()
        else:
            self._due_date = due_date

    def __str__(self):
        """String representation of the loan."""
        return (
            f"{self._item.to_short_string()} "
            f"(due: {self._due_date})"
        )
