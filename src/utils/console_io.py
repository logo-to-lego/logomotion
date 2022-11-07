"""Console IO"""


class ConsoleIO:
    """Class for IO operations"""

    @staticmethod
    def read(input_message=""):
        """Prints input message and returns input value"""
        return input(input_message)

    @staticmethod
    def write(message):
        """Prints given message"""
        print(message)

    @staticmethod
    def print_ast(ast, indent=""):
        """Prints ast as formatted string"""
        print(indent + "Type: " + str(ast.node_type))
        print(indent + "Leaf: " + str(ast.leaf))
        print(indent + "Logotype: " + str(ast.get_logotype()))
        print(indent + "Children: ")
        for child in ast.children:
            default_console_io.print_ast(child, indent + "\t")


default_console_io = ConsoleIO()
