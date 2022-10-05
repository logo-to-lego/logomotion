import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer
from parser.parser import Parser
from parser import ast
from entities.error_handler import ErrorHandler


class TestErrorHandler(unittest.TestCase):
    """Test class for testing error handler"""

    def setUp(self):
        self.console_mock = Mock()
        self.lexer = Lexer(console_io=self.console_mock)
        self.lexer.build()

        self.error_handler = ErrorHandler(console_io=self.console_mock)
        self.parser = Parser(
            current_lexer=self.lexer, console_io=self.console_mock, error_handler=self.error_handler
        )
        self.parser.build()

    def test_error_with_invalid_make_keyword(self):
        test_string = """mak "asd 123"""

        self.parser.parse(test_string)
        fin_expected_msg = (
            "En saanut selvää komennosta 'mak'. Löysin tämän riviltä 1 ja sarakkeelta 3."
        )
        eng_expected_msg = "I could not understand 'mak'. I found this on row 1 and column 3."

        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)
