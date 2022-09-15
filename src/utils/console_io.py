"""Console IO"""
class ConsoleIO:
    """Class for IO operations
    """

    @staticmethod
    def read(input_message=""):
        """Prints input message and returns input value
        """
        return input(input_message)

    @staticmethod
    def write(message):
        """Prints given message"""
        print(message)

default_console_io = ConsoleIO()

