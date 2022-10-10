import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer
from parser.parser import Parser
from utils.error_handler import ErrorHandler
from utils.logger import Logger
from entities.symbol_tables import SymbolTables
from entities.symbol_table import SymbolTable


class TestErrorHandler(unittest.TestCase):
    """Test class for testing error handler"""

    def setUp(self):
        self.console_mock = Mock()
        self.error_handler = ErrorHandler(console_io=self.console_mock)
        self.logger = Logger(self.console_mock, self.error_handler)
        self.lexer = Lexer(self.logger)
        self.lexer.build()
        self.symbol_tables = SymbolTables(SymbolTable(), SymbolTable())

        self.parser = Parser(self.lexer, self.logger, self.symbol_tables)
        self.parser.build()

    def test_error_with_invalid_make_keyword(self):
        test_string = """mak "asd 123"""

        self.parser.parse(test_string)
        fin_expected_msg = (
            "En saanut selvää komennosta 'mak'. Löysin tämän riviltä 1 ja sarakkeelta 3."
        )
        eng_expected_msg = "I could not understand 'mak'. I found this on row 1 and column 3."

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_error_with_invalid_binop(self):
        test_string = """
            make "a "kissa
            make "b 1 + :a
            """

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = "Rivillä 3 yritit tehdä laskutoimituksen jollakin joka ei ole numero."
        eng_expected_msg = "In row 3 you tried to calculate with something that is not a number."

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_invalid_unary_op_with_bool(self):
        test_string = """
            make "a -false
            """

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = "Negatiivisen luvun tyyppi on BOOL, vaikka sen pitäisi olla FLOAT."
        eng_expected_msg = "The type of a negative number is BOOL, even though it should be FLOAT."

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_invalid_unary_op_with_str(self):
        test_string = """
            make "a -"kissa
            """

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = "Negatiivisen luvun tyyppi on STRING, vaikka sen pitäisi olla FLOAT."
        eng_expected_msg = (
            "The type of a negative number is STRING, even though it should be FLOAT."
        )

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_relop_raises_error_with_unknown_type(self):
        test_string = """make "c :a >= :b"""

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = "Rivillä 1 en pystynyt päättelemään vertailuoperaattorin tyyppiä."
        eng_expected_msg = "In row 1 I could not infer the type of the operand."

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_relop_raises_error_with_non_comparable_types(self):
        test_string = """
            make "a "abc
            make "b 123
            make "c :a >= :b
            """

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = "Rivillä 4 koitit vertailla tyyppejä STRING ja FLOAT. Katso, että tyypit ovat keskenään samat."
        eng_expected_msg = "In row 4 you tried to compare types STRING and FLOAT. Check that you are comparing the same types."

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_valid_logo_code_does_not_yield_errors(self):
        test_string = """
            make "a 123
            show :a
            make "b true
        """

        ast = self.parser.parse(test_string)
        ast.check_types()

        self.assertEqual(len(self.error_handler.get_error_messages()), 0)
