import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer
from parser.parser import Parser
from parser import ast
from utils.error_handler import ErrorHandler
from utils.logger import Logger


class TestErrorHandler(unittest.TestCase):
    """Test class for testing error handler"""

    def setUp(self):
        self.console_mock = Mock()
        self.error_handler = ErrorHandler(console_io=self.console_mock)
        self.logger = Logger(self.console_mock, self.error_handler)
        self.lexer = Lexer(self.logger)
        self.lexer.build()

        self.parser = Parser(self.lexer, self.logger)
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
