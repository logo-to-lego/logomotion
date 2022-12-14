"""File to handle tests created with Robot Framework"""
import os
import subprocess
from parser.parser import Parser
from entities.symbol_tables import SymbolTables
from entities.symbol_table import SymbolTable
from entities.preconfigured_functions import initialize_logo_functions
from lexer.lexer import Lexer
from code_generator.code_generator import JavaCodeGenerator
from utils.error_handler import ErrorHandler
from utils.logger import Logger
from code_generator.preconf_code_generator import JavaPreconfFuncsGenerator

CWD = os.getcwd()
LOGO_TEST_PATH = os.path.join(CWD, "src/tests/e2e/test_files/")
JAVA_GEN_PATH = os.path.join(CWD, "src/tests/e2e/java/logo/")


class MockIO:
    def __init__(self) -> None:
        self._messages = []

    def write(self, message):
        self._messages.append(message)

def build_java_code_generator(logger):
    preconf_gen = JavaPreconfFuncsGenerator()
    jcg = JavaCodeGenerator(logger=logger)
    preconf_gen.set_code_generator(jcg)
    funcs_dict = preconf_gen.get_funcs()
    jcg.set_preconf_funcs_dict(funcs_dict)
    jcg.add_env_variables(
        wheelDiameter=os.getenv("WHEEL_DIAM"),
        wheelDistance=os.getenv("AXLE_LEN"),
        leftMotor=os.getenv("LEFT_MOTOR_PORT"),
        rightMotor=os.getenv("RIGHT_MOTOR_PORT"),
        motorSpeed=os.getenv("MOVEMENT_SPD"),
        motorRotationSpeed = os.getenv("ROTATION_SPD"),
    )
    return jcg


class AppLibrary:
    def __init__(self):
        # Compiler classes
        self._console_io = MockIO()
        self._error_handler = ErrorHandler(console_io=self._console_io)
        self._logger = Logger(self._console_io, self._error_handler)
        self._lexer = Lexer(self._logger)
        self._lexer.build()
        self._symbol_tables = SymbolTables(SymbolTable(), SymbolTable())
        self._java_code_generator = build_java_code_generator(self._logger)
        self._parser = Parser(
            self._lexer, self._logger, self._symbol_tables, self._java_code_generator
        )
        self._symbol_tables.functions = initialize_logo_functions(self._symbol_tables.functions)


    def _get_file_as_str(self, path):
        with open(path) as f:
            return f.read()

    def compile_logo(self, filepath):
        """Compiles the logocode (located in e2e/test_files/logo/filepath)"""
        path = os.path.join(LOGO_TEST_PATH, filepath)
        logocode = self._get_file_as_str(path)

        # Compile logo
        ast = self._parser.parse(logocode)
        ast.check_types()

        # Code generation, if there are no errors
        if not self._error_handler.errors:
            ast.generate_code()
            self._java_code_generator.write(JAVA_GEN_PATH)
        else:
            raise AssertionError(f"Given logocode in {filepath} is not valid", self._error_handler.errors)

    def java_compiles(self):
        """Compiles the generated java code (located in e2e/java/logo/Logo.java).
        Raises AssertionError if the compilation fails."""
        path = os.path.join(JAVA_GEN_PATH, "..")
        os.chdir(path)  # Change dir to make the compile
        output = subprocess.run(["javac", "logo/Logo.java"], capture_output=True) # Compile java
        os.chdir(CWD)  # Change dir back to make tests work after this
        if output.returncode != 0:
            raise AssertionError("Java compilation failed: \n", output.stderr.decode("utf-8"))
