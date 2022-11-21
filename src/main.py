"""Main module for the compiler.
"""
import argparse
import os
from parser.parser import Parser
import dotenv
from entities.symbol_tables import SymbolTables
from entities.preconfigured_functions import initialize_logo_functions
from lexer.lexer import Lexer
from utils.code_generator import JavaCodeGenerator
from utils.preconf_code_generator import JavaPreconfFuncsGenerator
from utils.console_io import ConsoleIO
from utils.error_handler import ErrorHandler
from utils.logger import Logger


def main():
    def get_code_generator():
        """Checks that given programming language is valid in
        .env file and returns a new instance of CodeGenerator class"""

        if CODE_GEN_LANG == "Java":
            preconf_gen = JavaPreconfFuncsGenerator()
            jcg = JavaCodeGenerator(logger=logger)
            preconf_gen.give_code_generator(jcg)
            funcs_dict = preconf_gen.get_funcs()
            jcg.give_preconf_funcs_dict(funcs_dict)
            return jcg
        err_msg = f"{CODE_GEN_LANG} is not an implemented" "programming language for code generator"
        raise Exception(err_msg)

    def compile_logo():
        """Compiles a user given logo file and generates code if there are no errors.
        Prints lexer & parser results if debug flag (-d, --debug) is on."""

        logger.debug(LOGO_CODE + "\n")
    
        # Tokenize
        tokens = lexer.tokenize_input(LOGO_CODE)
        logger.debug("Lexer tokens:")
        logger.debug("\n".join((str(token) for token in tokens)) + "\n")

        # Parse and type analyzation
        start_node = parser.parse(LOGO_CODE)
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

    # Create required classes for the compiler
    console_io = ConsoleIO()
    error_handler = ErrorHandler(console_io=console_io, language=MESSAGE_LANG)
    logger = Logger(console_io, error_handler, args.debug)
    lexer = Lexer(logger)
    lexer.build()
    symbol_tables = SymbolTables()
    code_generator = get_code_generator()
    parser = Parser(lexer, logger, symbol_tables, code_generator)
    parser.build()

    symbol_tables = initialize_logo_functions(symbol_tables)

    # Compile from logo to language defined with CODE_GEN .env variable
    compile_logo()


if __name__ == "__main__":

    def get_cmd_line_args():
        arg_parser = argparse.ArgumentParser(
            prog="Logomotion", description="Compile logo to java via python"
        )
        arg_parser.add_argument("filepath")
        arg_parser.add_argument("-d", "--debug", action="store_true")
        return arg_parser.parse_args()

    def load_file(filename):
        """Loads a file and returns contents as a string."""
        content = []
        with open(filename, "r", encoding="utf8") as file:
            content = file.readlines()
        return "".join(content)

    # Load variables from .env file
    dotenv.load_dotenv()
    MESSAGE_LANG = os.getenv("MESSAGE_LANG")
    CODE_GEN_LANG = os.getenv("CODE_GEN_LANG")

    # Get command line arguments
    args = get_cmd_line_args()

    # Get logo code from file. Filepath is given as a command line argument
    LOGO_CODE = load_file(args.filepath)

    main()
