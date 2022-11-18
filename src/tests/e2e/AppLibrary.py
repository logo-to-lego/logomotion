
class AppLibrary:
    def __init__(self):
        self._counter = 0

    def increase_counter(self):
        self._counter += 1

    def increment_counter_by(self, amount):
        int_amount = int(amount)
        self._counter += int_amount

    def counter_value_should_be(self, expected):
        int_expected = int(expected)
        if self._counter != int_expected:
            raise AssertionError(f"{self._counter} != {int_expected}")

# import argparse
# import os
# from parser.parser import Parser
# import dotenv
# from entities.symbol_tables import SymbolTables
# from entities.symbol_table import SymbolTable
# from entities.preconfigured_functions import initialize_logo_functions
# from lexer.lexer import Lexer
# from utils.code_generator import JavaCodeGenerator
# from utils.console_io import ConsoleIO
# from utils.error_handler import ErrorHandler
# from utils.logger import Logger


# class MockIO():
#     def __init__(self) -> None:
#         self._messages = []
    
#     def write(self, message):
#         self._messages.append(message)


# class AppLibrary:
#     def __init__(self):
#         self._console_io = MockIO()
#         self._error_handler = ErrorHandler(console_io=self._console_io)
#         self._logger = Logger(self._console_io, self._error_handler)
#         self._lexer = Lexer(self._logger)
#         self._lexer.build()
#         self._symbol_tables = SymbolTables(SymbolTable(), SymbolTable())
#         self._java_code_generator = JavaCodeGenerator(logger=self._logger)

#         self._parser = Parser(self._lexer, self._logger, self._symbol_tables, self._java_code_generator)
#         self._parser.build()


#     def compile_logo(self, logocode):
#         # start_node = self._parser.parse(logocode)
#         # start_node.check_types()
#         print("STUFF")

#     def increase_counter():
#         pass

#     def counter_value_should_be(self, value):
#         pass