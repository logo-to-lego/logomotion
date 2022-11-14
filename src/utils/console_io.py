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
    def get_formatted_ast(ast, indent="", result=""):
        result += indent + "Type: " + str(ast.node_type) + "\n"
        result += indent + "Leaf: " + str(ast.leaf) + "\n"
        result += indent + "Logotype: " + str(ast.get_logotype()) + "\n"
        result += indent + "Children: " + "\n"
        for child in ast.children:
            result += default_console_io.get_formatted_ast(child, (indent + "\t"))
        return result

    @staticmethod
    def print_ast(ast):
        """Prints ast as formatted string"""
        print(default_console_io.get_formatted_ast(ast))


default_console_io = ConsoleIO()
