"""
Borrowable item module for library system.
"""


class BorrowableItem:
    """
    Represents an item that can be borrowed from the library.
    """

    def __init__(self, item_id, name, item_type, num_copies=1, on_loan=0, location="Main Library"):
        # pylint: disable=too-many-arguments
        # Six parameters are necessary for complete item initialization
        """
        Initialize a BorrowableItem.

        Args:
            item_id: Unique identifier for the item
            name: Name of the item
            item_type: Type/category of the item
            num_copies: Total number of copies available
            on_loan: Number of copies currently on loan
            location: Physical location of the item
        """
        self._id = item_id
        self._name = name
        self._type = item_type
        self._num_copies = num_copies
        self._on_loan = on_loan
        self._location = location

    def is_available(self):
        """
        Check if the item is available for loan.

        Returns:
            Boolean indicating availability
        """
        return self._on_loan < self._num_copies

    def __str__(self):
        """String representation of the item."""
        available = self._num_copies - self._on_loan
        return (
            f"{self._name} (ID: {self._id}, Type: {self._type}, "
            f"Available: {available}/{self._num_copies}, Location: {self._location})"
        )
