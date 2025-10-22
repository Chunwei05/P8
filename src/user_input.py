"""
User input validation and handling functions.
"""


def get_menu_choice(prompt, valid_choices):
    """
    Get a valid menu choice from the user.

    Args:
        prompt: The prompt to display
        valid_choices: List of valid choice strings

    Returns:
        The validated user choice
    """
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice. Please choose from: {valid_choices}")


def get_string_input(prompt):
    """
    Get a non-empty string input from the user.

    Args:
        prompt: The prompt to display

    Returns:
        The user's input string
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_int_input(prompt):
    """
    Get an integer input from the user.

    Args:
        prompt: The prompt to display

    Returns:
        The validated integer
    """
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_int_input_in_range(prompt, min_value, max_value):
    """
    Get an integer input within a specified range.

    Args:
        prompt: The prompt to display
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        The validated integer within range
    """
    while True:
        value = get_int_input(prompt)
        if min_value <= value <= max_value:
            return value
        print(
            f"Input must be between {min_value} and {max_value}. "
            f"Please try again."
        )


def get_float_input(prompt):
    """
    Get a float input from the user.

    Args:
        prompt: The prompt to display

    Returns:
        The validated float
    """
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_float_input_in_range(prompt, min_value, max_value):
    """
    Get a float input within a specified range.

    Args:
        prompt: The prompt to display
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        The validated float within range
    """
    while True:
        value = get_float_input(prompt)
        if min_value <= value <= max_value:
            return value
        print(
            f"Input must be between {min_value} and {max_value}. "
            f"Please try again."
        )


def get_yes_no_input(prompt):
    """
    Get a yes/no input from the user.

    Args:
        prompt: The prompt to display

    Returns:
        True for 'y', False for 'n'
    """
    while True:
        line = input(prompt).strip().lower()
        if line in ('y', 'n'):
            return line == 'y'
        print("Invalid input. Please enter 'y' or 'n'.")
