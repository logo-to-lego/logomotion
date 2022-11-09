"""Main module for the compiler.
"""
import argparse
from parser.parser import Parser
from entities.symbol_tables import SymbolTables
from lexer.lexer import Lexer
from utils.code_generator import CodeGenerator
from utils.console_io import ConsoleIO
from utils.error_handler import ErrorHandler
from utils.logger import Logger


def main(filepath: str, debug: bool):
    def load_file(filename):
        """Loads a file and returns contents as a string."""
        content = []
        with open(filename, "r", encoding="utf8") as file:
            content = file.readlines()
        return "".join(content)

    def file_parser():
        """Parses a user given file and prints lexer & parser results."""
        code = load_file(filepath)

        logger.debug(f"Load file {filepath}:")
        logger.debug(code + "\n")
        logger.debug("Lexer tokens:")
        logger.debug("\n".join((str(token)
            for token in lexer.tokenize_input(code))) + "\n")
        logger.debug("Parser AST:")

        start_node = parser.parse(code)
        start_node.check_types()
        start_node.generate_code()

        if debug:
            console_io.print_ast(start_node)

        error_handler.write_errors_to_console()
        code_generator.write()


    console_io = ConsoleIO()
    error_handler = ErrorHandler(console_io=console_io, language="FIN")
    logger = Logger(console_io, error_handler, debug)

    lexer = Lexer(logger)
    lexer.build()

    symbol_tables = SymbolTables()
    code_generator = CodeGenerator(logger=logger)

    parser = Parser(lexer, logger, symbol_tables, code_generator)
    parser.build()

    file_parser()



if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        prog="Logomotion",
        description="Compile logo to java via python")
    arg_parser.add_argument("filepath")
    arg_parser.add_argument("-d", "--debug", action="store_true")
    args = arg_parser.parse_args()

    main(args.filepath, args.debug)
