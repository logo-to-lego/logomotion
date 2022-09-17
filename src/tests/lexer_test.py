import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer


class TestLexer(unittest.TestCase):
    """Test class for testing lexer.lexer.Lexer"""

    def setUp(self):
        self.console_mock = Mock()
        self.lexer = Lexer(console_io=self.console_mock)
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

    def test_token_does_not_increase_line_number_from_comments(self):
        test_string = """; This is a comment
        This is not."""

        self.token_mock.value = test_string
        self.assertEqual(self.token_mock.lexer.lineno, 0)
        self.lexer.t_ignore_comment(self.token_mock)
        self.assertEqual(self.token_mock.lexer.lineno, 0)

    def test_commented_lines_increase_line_number_by_only_one(self):
        test_string = """ABC
        ; This is a comment
        DEF"""

        lexer = self.lexer.get_lexer()
        lexer.input(test_string)
        token_abc = lexer.token()
        self.assertEqual(token_abc.lineno, 1)
        token_def = lexer.token()
        self.assertEqual(token_def.lineno, 3)

    def test_lexer_finds_illegal_characters(self):
        test_string = 'make % "travel.distance 10'

        lexer = self.lexer.get_lexer()
        lexer.input(test_string)

        for token in lexer:
            pass

        self.console_mock.write.assert_called()
        self.assertIn("Illegal", self.console_mock.write.call_args.args[0])
