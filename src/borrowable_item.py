"""
Module for BorrowableItem class.
"""


class BorrowableItem:
    """
    Represents an item that can be borrowed from the library.
    """

    def __init__(self, item_id, name, item_type, year, number_owned):
        """
        Initialize a BorrowableItem.

        Args:
            item_id: Unique identifier for the item
            name: Name of the item
            item_type: Type/category of the item
            year: Year of publication/creation
            number_owned: Total number of copies owned
        """
        self._id = item_id
        self._name = name
        self._type = item_type
        self._year = year
        self._number_owned = number_owned
        self._on_loan = 0

    @property
    def available(self):
        """Check if item is available for loan."""
        return self._number_owned - self._on_loan > 0

    def to_short_string(self):
        """Return a short string representation of the item."""
        return f"{self._type}: {self._name} ({self._year})"

    def to_full_string(self):
        """Return a full string representation of the item."""
        available_count = self._number_owned - self._on_loan
        return (
            f"{self._type}: {self._name} ({self._year}) - "
            f"{available_count}/{self._number_owned} available"
        )

    def __str__(self):
        """String representation of the item."""
        return self.to_short_string()

    def __repr__(self):
        """Developer-friendly representation of the item."""
        return (
            f"BorrowableItem(id={self._id}, name='{self._name}', "
            f"type='{self._type}', year={self._year})"
        )
