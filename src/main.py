"""Main module for the compiler.
"""
import sys
from parser.parser import Parser
from lexer.lexer import Lexer
from utils.console_io import ConsoleIO
from entities.error_handler import ErrorHandler


io = ConsoleIO(debug=True)
error_handler = ErrorHandler(console_io=io, language="FIN")

lexer = Lexer(console_io=io)
lexer.build()

parser = Parser(lexer, console_io=io, error_handler=error_handler)
parser.build()


def parser_ui():
    """For parser testing."""
    while True:
        program = []

        io.write("Enter logo code, an empty line to start parsing or q! to quit:")

        while True:
            user_input = io.read()

            if user_input == "q!":
                sys.exit()

            if not user_input:
                break

            program.append(user_input)

        code = "\n".join(program)
        io.write("Lexer tokens:")
        io.write("\n".join((str(token) for token in lexer.tokenize_input(code))) + "\n")
        io.write("AST Result:")
        io.write(parser.parse(code))
        error_handler.write_errors_to_console()


def load_file(filename):
    """Loads a file and returns contents as a string."""
    content = []

    with open(filename, "r", encoding="utf8") as file:
        content = file.readlines()

    return "".join(content)


def file_parser():
    """Parses a user given file and prints lexer & parser results."""
    filename = sys.argv[1]
    code = load_file(filename)
    io.write(f"Load file {filename}:")
    io.write(code + "\n")
    io.write("Lexer tokens:")
    io.write("\n".join((str(token) for token in lexer.tokenize_input(code))) + "\n")
    io.write("Parser AST:")
    io.write(parser.parse(code))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_parser()
    else:
        USE_UI = True

        if USE_UI:
            parser_ui()
        else:
            PROG = """fd 2 bk 50 rt 1+2 lt :a"""
            ast = parser.parse(PROG)
            io.write(ast)
            error_handler.write_errors_to_console()
