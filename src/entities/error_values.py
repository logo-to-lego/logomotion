# pylint: disable=too-few-public-methods
"""Module for the ErrorValue class"""


class ErrorValues:
    """Class to keep track error values to AST nodes"""

    def __init__(self):
        """Initialize a new ErrorValues object"""
        self.errors = []

    def add_error(self, error):
        """Add a new error to the value list
        Args:
            error: The ErrorInfo object to add to the list"""

        self.errors.append(error)
