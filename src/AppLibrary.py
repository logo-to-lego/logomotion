"""File to handle tests created with Robot Framework"""
import argparse
import os
import subprocess
from parser.parser import Parser
import dotenv
from entities.symbol_tables import SymbolTables
from entities.symbol_table import SymbolTable
from entities.preconfigured_functions import initialize_logo_functions
from lexer.lexer import Lexer
from utils.code_generator import JavaCodeGenerator
from utils.console_io import ConsoleIO
from utils.error_handler import ErrorHandler
from utils.logger import Logger

JAVA_GEN_PATH = os.path.join(
    os.path.dirname(os.path.relpath(__file__)), "tests/e2e/java/logo/"
)

JAVA_TEST_PATH = os.path.join(
    os.path.dirname(os.path.relpath(__file__)), "tests/e2e/test_files/java/"
)

LOGO_TEST_PATH = os.path.join(
    os.path.dirname(os.path.relpath(__file__)), "tests/e2e/test_files/logo/"
)


class MockIO():
    def __init__(self) -> None:
        self._messages = []
    
    def write(self, message):
        self._messages.append(message)


class AppLibrary:
    def __init__(self):
        # Compiler classes
        self._console_io = MockIO()
        self._error_handler = ErrorHandler(console_io=self._console_io)
        self._logger = Logger(self._console_io, self._error_handler)
        self._lexer = Lexer(self._logger)
        self._lexer.build()
        self._symbol_tables = SymbolTables(SymbolTable(), SymbolTable())
        self._java_code_generator = JavaCodeGenerator(logger=self._logger)
        self._parser = Parser(self._lexer, self._logger, self._symbol_tables, self._java_code_generator)
        self._parser.build()

    def _get_file_as_str(self, path):
        with open(path) as f:
            return f.read()

    def compile_logo(self, filename):
        """Compiles the logocode (located in e2e/test_files/logo)"""
        path = os.path.join(LOGO_TEST_PATH, filename)
        logocode = self._get_file_as_str(path)

        # Compile logo
        ast = self._parser.parse(logocode)
        ast.check_types()

        # Code generation, if there are no errors
        if not self._error_handler.errors:
            ast.generate_code()
            self._java_code_generator.write(JAVA_GEN_PATH)
        else:
            raise AssertionError(f"Given logocode in {filename} is not valid")

    def _difference(self, str1, str2):
        # Split both strings into list items
        str1 = str1.split()
        str2 = str2.split()
        A = set(str1)
        B = set(str2)
        return A.symmetric_difference(B)

    def java_is_valid(self, filename):
        """Compares the test java file (located in e2e/test_files/java) and generated java.
        Raises AssertionError if the test code and generated code do not match.
        The comparison is done simply by comparing the strings without spaces, tabs or newlines"""
        test_java_path = os.path.join(JAVA_TEST_PATH, filename)
        generated_java_path = os.path.join(JAVA_GEN_PATH, "Logo.java")
        
        test_java_code = self._get_file_as_str(test_java_path)
        generated_java_code = self._get_file_as_str(generated_java_path)

        # Remove spaces, tabs and new lines
        code1 = ''.join(test_java_code.split())
        code2 = ''.join(generated_java_code.split())

        if code1 != code2:
            difference = self._difference(test_java_code, generated_java_code)
            raise AssertionError(f"{filename} and generated java did not match: ", difference)

    def java_compiles(self):
        """Compiles the generated java code (located in e2e/java/logo/Logo.java).
        Raises AssertionError if the compilation failes."""
        path = os.path.join(JAVA_GEN_PATH, "..")
        os.chdir(path)
        output = subprocess.run(['javac', 'logo/Logo.java'], capture_output=True)
        if output.returncode != 0:
            raise AssertionError("Java compilation failed: ", output.stderr.decode('utf-8'))