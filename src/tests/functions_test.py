"""Test module for type check in functions.py (and statementlist.py)"""
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
    function calls and output commands in functions.py (and statementlist.py)"""

    def setUp(self):
        console_io = Mock()
        self.error_handler = ErrorHandlerMock()
        self.logger = Logger(console_io=console_io, error_handler=self.error_handler)
        self.lexer = Lexer(self.logger)
        self.lexer.build()
        self.symbol_tables = SymbolTables(SymbolTable(), SymbolTable())
        self.parser = Parser(self.lexer, self.logger, self.symbol_tables)

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

    def test_output_of_deref_does_not_cause_error_in_output(self):
        test_code = """TO f :x make "y :x+1 output :y END"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(0, len(self.error_handler.get_error_ids()))

    def test_output_of_undefined_deref_cause_error(self):
        test_code = """TO f :x if :x > 0 { output :y } output :y END"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(True, self.error_handler.check_id_is_in_errors(2007))

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

    def test_function_doesnt_end_to_output_if_it_has_output_elsewhere_procdecl(self):
        test_code = """TO f :x if :x > 1 { output :x+1 } END"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(True, self.error_handler.check_id_is_in_errors(2027))

    def test_make_statement_works_in_functions(self):
        test_code = """TO f :x if :x > 0 { make "x :x-1 output :x }
                    make "x :x+1 output :x END"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(0, len(self.error_handler.get_error_ids()))
    

    def test_function_calls_argument_is_not_right_type_in_proccall_when_parameter_type_is_unknown(self):
        test_code = """TO f :a output :a END make "a (f 3)"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(True, self.error_handler.check_id_is_in_errors(2026))

    def test_function_calls_are_case_insensitive(self):
        test_code = """TO Test output 1 END make "x (tEST)"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(len(self.error_handler.error_ids), 0)

    def test_function_params_are_case_insensitive(self):
        test_code = """TO test.func :test.param make "x :tEST.pARAM+0 END"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(len(self.error_handler.error_ids), 0)

    def test_function_return_value_can_be_stored_in_a_variable(self):
        test_code = """TO f :a :b output :a + :b END make "c (f 1 2)"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        var = self.symbol_tables.variables.lookup('c')
        self.assertIsNotNone(var)

    def test_function_return_value_can_be_stored_in_a_variable_as_unary(self):
        test_code = """TO f :a :b output :a + :b END make "c -(f 1 2)"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        var = self.symbol_tables.variables.lookup('c')
        self.assertIsNotNone(var)

    def test_function_param_types_update_with_move_commands(self):
        test_code = """TO f :a fd :a END (f 5)"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(0, len(self.error_handler.get_error_ids()))

    def test_proccall_with_arguments_in_procdecl_doesnt_cause_type_errors(self):
        test_code = """TO f :x output :x+0 END TO g :y output f :y END g f 1"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        errors = self.error_handler.get_error_ids()
        self.assertEqual(0, len(errors))

    def test_recursion_call_in_func_decl_infers_type(self):
        test_code = """TO f :x :y f "kissa 42 end"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        errors = self.error_handler.get_error_ids()
        self.assertEqual(0, len(errors))
    
    def test_binop_sets_type_in_recursive_call(self):
        test_code = """TO f :y MAKE "x 1+f :y OUTPUT :y END"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        errors = self.error_handler.get_error_ids()
        self.assertEqual(0, len(errors))