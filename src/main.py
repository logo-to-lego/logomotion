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

    def compile():
        """Parses a user given file and prints lexer & parser results."""

        # Get file
        code = load_file(filepath)
        logger.debug(f"Load file {filepath}:")
        logger.debug(code + "\n")
        
        # Tokenize
        tokens = lexer.tokenize_input(code)
        logger.debug("Lexer tokens:")
        logger.debug("\n".join((str(token) for token in tokens)) + "\n")

        # Parse and type analyzation
        start_node = parser.parse(code)
        start_node.check_types()
        logger.debug("Parser AST:")
        logger.debug(console_io.get_formatted_ast(start_node))
        
        # Code generation, if there are no errors
        if not error_handler.errors:
            logger.debug("Generated code:")
            start_node.generate_code()
            code_generator.write()
        else:
            error_handler.write_errors_to_console()


    console_io = ConsoleIO()
    error_handler = ErrorHandler(console_io=console_io, language="FIN")
    logger = Logger(console_io, error_handler, debug)

    lexer = Lexer(logger)
    lexer.build()

    symbol_tables = SymbolTables()
    code_generator = CodeGenerator(logger=logger)

    parser = Parser(lexer, logger, symbol_tables, code_generator)
    parser.build()

    compile()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        prog="Logomotion",
        description="Compile logo to java via python")
    arg_parser.add_argument("filepath")
    arg_parser.add_argument("-d", "--debug", action="store_true")
    args = arg_parser.parse_args()

    main(args.filepath, args.debug)
