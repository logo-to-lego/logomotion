"""Main module for the compiler.
"""
import sys
from parser.parser import Parser
from lexer.lexer import Lexer
from utils.console_io import default_console_io as io


lexer = Lexer()
lexer.build()

parser = Parser(lexer)
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

        io.write(parser.parse("\n".join(program)))


USE_UI = True

if USE_UI:
    parser_ui()
else:
    PROG = """fd 2 bk 50 rt 1+2 lt :a"""
    ast = parser.parse(PROG)
    io.write(ast)
