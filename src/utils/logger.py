"""Module for console printing and error handling."""
from utils.console_io import default_console_io
from utils.error_handler import default_error_handler


class Logger:
    """Console IO/Error Handling utilities"""

    def __init__(
        self, console_io=default_console_io, error_handler=default_error_handler, debug=False
    ):
        self.console = console_io
        self.error_handler = error_handler
        self._debug = debug

    def debug(self, input_message=""):
        """Prints a debug message using console_io if the DEBUG flag is set."""
        if self._debug:
            self.console.write(input_message)


default_logger = Logger()
