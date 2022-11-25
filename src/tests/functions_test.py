"""Test module for type check in functions.py"""
from entities.symbol_table import SymbolTable
from entities.symbol_tables import SymbolTables
from lexer.lexer import Lexer
from parser.parser import Parser
from unittest.mock import Mock
from utils.error_handler_mock import ErrorHandlerMock
from utils.logger import Logger
import unittest


class TestFunctions(unittest.TestCase):
    """Test class for testing type checking and errors of function declarations,
    function calls and output commands in functions.py"""

    def setUp(self):
        console_io = Mock()
        self.error_handler = ErrorHandlerMock()
        self.logger = Logger(console_io=console_io, error_handler=self.error_handler)
        self.lexer = Lexer(self.logger)
        self.lexer.build()
        symbol_tables = SymbolTables(SymbolTable(), SymbolTable())
        self.parser = Parser(self.lexer, self.logger, symbol_tables)
        self.parser.build()

    def test_function_has_already_been_made_in_procdecl(self):
        test_code = "TO f END TO f END"
        ast = self.parser.parse(test_code)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()
        self.assertListEqual(error_ids, [2017])

    def test_function_parameter_type_is_unknown_in_procdecl(self):
        test_code = "TO f :x END"
        ast = self.parser.parse(test_code)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()
        self.assertListEqual(error_ids, [2019])

    def test_function_parameter_already_exists_in_procarg(self):
        test_code = "TO f :x :x END"
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(True, self.error_handler.check_id_is_in_errors(2018))

    def test_output_command_is_not_in_a_function_in_output(self):
        test_code = "TO f END output 1"
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(True, self.error_handler.check_id_is_in_errors(2024))

    def test_output_values_types_do_not_vary_in_output(self):
        test_code = """TO f if true { output 1 } output "a END"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(True, self.error_handler.check_id_is_in_errors(2025))

    def test_deref_output_does_not_cause_error_in_output(self):
        test_code = """TO f :x make "y :x+1 output :y END"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(0, len(self.error_handler.get_error_ids()))

    def test_function_call_has_too_much_arguments_in_proccall(self):
        test_code = """TO f :x output :x+1 END (f 1 2)"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(True, self.error_handler.check_id_is_in_errors(2021))

    def test_function_call_has_too_few_arguments_in_proccall(self):
        test_code = """TO f :x :y output :x+:y+1 END (f 1)"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(True, self.error_handler.check_id_is_in_errors(2021))

    def test_called_function_does_not_exists_in_proccall(self):
        test_code = """TO f END (g)"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(True, self.error_handler.check_id_is_in_errors(2020))

    def test_function_calls_argument_is_not_right_type_in_proccall(self):
        test_code = """TO f :x output :x+1 END (f true)"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(True, self.error_handler.check_id_is_in_errors(2022))
    
    def test_function_calls_argument_is_not_right_type_in_proccall_when_parameter_type_is_unknown(self):
        test_code = """TO f :a output :a END make "a (f 3)"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(True, self.error_handler.check_id_is_in_errors(2026))
