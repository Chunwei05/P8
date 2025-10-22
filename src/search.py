"""
Search functionality for patrons and items.
"""


def search_patron_by_name(patron_list, name):
    """
    Search for a patron by name.

    Args:
        patron_list: List of Patron objects
        name: Name to search for

    Returns:
        Patron object if found, None otherwise
    """
    for patron in patron_list:
        if patron._name.lower() == name.lower():
            return patron
    return None


def search_patron_by_id(patron_list, patron_id):
    """
    Search for a patron by ID.

    Args:
        patron_list: List of Patron objects
        patron_id: ID to search for

    Returns:
        Patron object if found, None otherwise
    """
    for patron in patron_list:
        if patron._id == patron_id:
            return patron
    return None


def search_patron_by_age(patron_list, age):
    """
    Search for patrons by age.

    Args:
        patron_list: List of Patron objects
        age: Age to search for

    Returns:
        List of Patron objects matching the age
    """
    results = []
    for patron in patron_list:
        if patron._age == age:
            results.append(patron)
    return results


def search_patron_by_name_and_age(patron_list, name, age):
    """
    Search for patrons by name and age.

    Args:
        patron_list: List of Patron objects
        name: Name to search for
        age: Age to search for

    Returns:
        List of Patron objects matching both criteria
    """
    results = []
    for patron in patron_list:
        if (patron._name.lower() == name.lower() and
                patron._age == age):
            results.append(patron)
    return results


def search_item_by_id(item_list, item_id):
    """
    Search for an item by ID.

    Args:
        item_list: List of BorrowableItem objects
        item_id: ID to search for

    Returns:
        BorrowableItem object if found, None otherwise
    """
    for item in item_list:
        if item._id == item_id:
            return item
    return None
