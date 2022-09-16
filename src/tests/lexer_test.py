import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer

class TestLexer(unittest.TestCase):
    """Test class for testing lexer.lexer.Lexer"""

    def setUp(self):
        self.lexer = Lexer()
        self.token_mock = Mock()
        self.token_mock.lexer.lineno = 0

    def tearDown(self):
        self.token_mock = Mock()

    def test_token_method_returns_numbers_correctly(self):
        self.token_mock.value = "123"
        tok = self.lexer.t_NUMBER(self.token_mock)
        self.assertEqual(tok.value, 123)

    def test_token_method_returns_identifiers_correctly(self):
        self.token_mock.value = "miten"
        identifier = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(identifier.type, "TO")

        self.token_mock.value = "right"
        identifier = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(identifier.type, "RT")

        self.token_mock.value = "lt"
        identifier = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(identifier.type, "LT")

        self.token_mock.value = "olkoon"
        identifier = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(identifier.type, "MAKE")

        self.token_mock.value = "blah"
        identifier = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(identifier.type, "IDENT")

    def test_token_counts_line_number_correctly(self):
        test_string = """Väinämöinen, old and steadfast,
        Answered in the words which follow:
        "Yet a harp might be constructed
        Even of the bones of fishes..."""
        
        self.token_mock.value = test_string
        self.assertEqual(self.token_mock.lexer.lineno, 0)
        self.lexer.t_ignore_newline(self.token_mock)
        self.assertEqual(self.token_mock.lexer.lineno, 3)

    def test_token_increases_line_number_from_comments(self):
        test_string = "; This is a comment"

        self.token_mock.value = test_string
        self.assertEqual(self.token_mock.lexer.lineno, 0)
        self.lexer.t_ignore_comment(self.token_mock)
        self.assertEqual(self.token_mock.lexer.lineno, 1)