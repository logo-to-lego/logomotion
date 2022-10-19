"""Main module for the compiler.
"""
import sys
from parser.parser import Parser
from entities.symbol_tables import SymbolTables
from entities.symbol_table import SymbolTable
from lexer.lexer import Lexer
from utils.code_generator import CodeGenerator
from utils.console_io import ConsoleIO
from utils.error_handler import ErrorHandler
from utils.logger import Logger

io = ConsoleIO()
error_handler = ErrorHandler(console_io=io, language="FIN")
logger = Logger(io, error_handler, debug=True)

lexer = Lexer(logger)
lexer.build()

symbol_tables = SymbolTables()
code_generator = CodeGenerator(logger=logger)

parser = Parser(lexer, logger, symbol_tables, code_generator)
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
        start_node = parser.parse(code)
        io.write(start_node)
        io.write("")

        start_node.check_types()
        io.write("Type checks:")
        io.write(start_node)

        error_handler.write_errors_to_console()
        error_handler.errors.clear()

        start_node.generate_code()
        code_generator.write()

        # Clear symbol tables
        symbol_tables.functions = SymbolTable()
        symbol_tables.variables = SymbolTable()


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
    start_node = parser.parse(code)
    io.write(start_node)
    start_node.check_types()
    io.write("\nType checks:")
    io.write(start_node)


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
