import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer
from parser.parser import Parser
from utils.error_handler import ErrorHandler
from utils.error_handler_mock import ErrorHandlerMock
from utils.logger import Logger
from entities.symbol_tables import SymbolTables
from entities.symbol_table import SymbolTable


class TestErrorHandler(unittest.TestCase):
    """Test class for testing error handler"""

    def setUp(self):
        self.console_mock = Mock()
        self.error_handler = ErrorHandlerMock()
        #self.error_handler = ErrorHandler(console_io=self.console_mock)
        self.logger = Logger(self.console_mock, self.error_handler)
        self.lexer = Lexer(self.logger)
        self.lexer.build()
        self.symbol_tables = SymbolTables(SymbolTable(), SymbolTable())

        self.parser = Parser(self.lexer, self.logger, self.symbol_tables)

    def test_valid_logo_code_does_not_yield_errors(self):
        test_string = """
            make "a 123
            show :a
            make "b true
        """

        ast = self.parser.parse(test_string)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [])

    def test_error_with_invalid_make_keyword(self):
        test_string = """mak "asd 123"""

        self.parser.parse(test_string)

        error_ids = self.error_handler.get_error_ids()
        self.assertListEqual(error_ids, [2000])

    def test_error_with_invalid_binop(self):
        test_string = """
            make "a "kissa
            make "b 1 + :a
            """

        ast = self.parser.parse(test_string)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [2002])

    def test_invalid_unary_op_with_bool(self):
        test_string = """
            make "a -false
            """

        ast = self.parser.parse(test_string)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [2003])

    def test_invalid_unary_op_with_str(self):
        test_string = """
            make "a -"kissa
            """

        ast = self.parser.parse(test_string)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [2003])


    def test_valid_relops_work(self):
        test_string = """
            make "a "kissa
            make "b 42
            make "c :a <> "koira
            make "d :b > 100
        """

        ast = self.parser.parse(test_string)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [])

    def test_relop_raises_error_with_undefined_variables(self):
        test_string = """make "c :a >= :b"""

        ast = self.parser.parse(test_string)
        ast.check_types()

        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [2007, 2007])

    def test_relop_raises_error_with_non_comparable_types(self):
        test_string = """
            make "a "abc
            make "b 123
            make "c :a >= :b
            """

        ast = self.parser.parse(test_string)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [2005])

    def test_variable_is_not_defined(self):
        test_string = """fd :x"""

        ast = self.parser.parse(test_string)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [2007])

    def test_move_commands_yield_error_with_invalid_parameter_type(self):
        test_string = """
            make "a "somevalue
            fd "abc
            bk true
            lt false
            rt :a
            """

        ast = self.parser.parse(test_string)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [2010, 2010, 2010, 2010])

    def test_make_only_accepts_string_as_variable_name(self):
        test_string = """
            make true "abc
            make 123 456
            make "foo "bar
        """

        ast = self.parser.parse(test_string)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [2010, 2010])

    def test_make_only_accepts_same_type_as_new_value(self):
        test_string = """
            make "a 123
            make "a "abc
            make "a true
            make "a 456
        """

        ast = self.parser.parse(test_string)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [2012, 2012])

    def test_make_raises_error_if_variable_name_is_deref(self):
        test_string = "make :muuttuja 42"

        ast = self.parser.parse(test_string)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()

        self.assertListEqual(error_ids, [2028])
