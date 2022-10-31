import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer
from parser.parser import Parser
from utils.error_handler import ErrorHandler
from utils.logger import Logger
from entities.symbol_tables import SymbolTables
from entities.symbol_table import SymbolTable


class TestType(unittest.TestCase):
    """test class for entities.symbol.Symbol and classes Variable
    and Function that inherits it"""

    def setUp(self):
        self.console_mock = Mock()
        self.error_handler = ErrorHandler(console_io=self.console_mock)
        self.logger = Logger(self.console_mock, self.error_handler)
        self.lexer = Lexer(self.logger)
        self.lexer.build()
        self.symbol_tables = SymbolTables(SymbolTable(), SymbolTable())

        self.parser = Parser(self.lexer, self.logger, self.symbol_tables)
        self.parser.build()

    def test_deref_adds_variable_to_same_instance_of_typeclass(self):
        test_string = """
            make "a 123
            make "b :a
        """
        ast = self.parser.parse(test_string)
        ast.check_types()

        typeclass_a = self.symbol_tables.variables.lookup("a").typeclass
        typeclass_b = self.symbol_tables.variables.lookup("b").typeclass
        self.assertEqual(id(typeclass_a), id(typeclass_b))

    def test_two_variables_have_different_instance_of_typeclass(self):
        test_string = """
            make "a 123
            make "b 456
        """
        ast = self.parser.parse(test_string)
        ast.check_types()

        typeclass_a = self.symbol_tables.variables.lookup("a").typeclass
        typeclass_b = self.symbol_tables.variables.lookup("b").typeclass
        self.assertNotEqual(id(typeclass_a), id(typeclass_b))

    def test_two_separate_typeclasses_with_different_types_should_not_concatenate_into_one(self):
        test_string = """
            make "a 2
            make "b "kissa
            make "a :b
        """
        ast = self.parser.parse(test_string)
        ast.check_types()

        typeclass_a = self.symbol_tables.variables.lookup("a").typeclass
        typeclass_b = self.symbol_tables.variables.lookup("b").typeclass

        self.assertNotEqual(id(typeclass_a), id(typeclass_b))

    def test_two_separate_typeclasses_concatenate_into_one(self):
        test_string = """
            make "a 2
            make "b :a

            make "c 5
            make "d :c

            make "d :a
        """
        ast = self.parser.parse(test_string)
        ast.check_types()

        typeclass_a = self.symbol_tables.variables.lookup("a").typeclass
        typeclass_b = self.symbol_tables.variables.lookup("b").typeclass
        typeclass_c = self.symbol_tables.variables.lookup("c").typeclass
        typeclass_d = self.symbol_tables.variables.lookup("d").typeclass

        self.assertEqual(id(typeclass_a), id(typeclass_b))
        self.assertEqual(id(typeclass_b), id(typeclass_c))
        self.assertEqual(id(typeclass_c), id(typeclass_d))
