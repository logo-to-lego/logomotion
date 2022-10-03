# pylint: disable=too-few-public-methods
"""Module for the ErrorInfo class"""


class ErrorInfo:
    """Class for storing AST node error information"""

    def __init__(self, node, error_message):
        """Initialize a new ErrorInfo object
        Args:
            node: The AST node that threw the error
            error_message: The error the AST node threw"""

        self.node = node
        self.error_message = error_message
