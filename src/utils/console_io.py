"""Console IO"""


class ConsoleIO:
    """Class for IO operations"""

    def __init__(self, debug=False):
        self._debug = debug

    def debug(self, input_message=""):
        """Prints a debug message if the DEBUG flag is set."""
        if self._debug:
            self.write(input_message)

    @staticmethod
    def read(input_message=""):
        """Prints input message and returns input value"""
        return input(input_message)

    @staticmethod
    def write(message):
        """Prints given message"""
        print(message)


default_console_io = ConsoleIO()
