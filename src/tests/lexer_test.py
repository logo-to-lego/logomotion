import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer
from lexer.token_types import TokenType


class TestLexer(unittest.TestCase):
    """Test class for testing lexer.lexer.Lexer"""

    def setUp(self):
        self.console_mock = Mock()
        self.lexer = Lexer(console_io=self.console_mock)
        self.ply_lexer = self.lexer.get_ply_lexer()
        self.token_mock = Mock()
        self.token_mock.lexer.lineno = 0
        self.token_mock.lexer.linestartpos = 0
        self.token_mock.lexpos = 0

    def tearDown(self):
        self.token_mock = Mock()

    def test_token_method_returns_floats_correctly(self):
        self.token_mock.value = "1.23"
        tok = self.lexer.t_FLOAT(self.token_mock)
        self.assertAlmostEqual(tok.value, 1.23)

        self.token_mock.value = "123.456"
        tok = self.lexer.t_FLOAT(self.token_mock)
        self.assertAlmostEqual(tok.value, 123.456)

    def test_token_method_returns_numbers_correctly(self):
        self.token_mock.value = "123"
        tok = self.lexer.t_NUMBER(self.token_mock)
        self.assertEqual(tok.value, 123)

    def test_token_method_returns_to_identifier_correctly(self):
        self.token_mock.value = "to"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "TO")

        self.token_mock.value = "miten"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "TO")

    def test_token_method_returns_end_identifier_correctly(self):
        self.token_mock.value = "end"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "END")

        self.token_mock.value = "valmis"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "END")

    def test_token_method_returns_fd_identifier_correctly(self):
        self.token_mock.value = "forward"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "FD")

        self.token_mock.value = "fd"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "FD")

        self.token_mock.value = "eteen"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "FD")

        self.token_mock.value = "et"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "FD")

    def test_token_method_returns_bk_identifier_correctly(self):
        self.token_mock.value = "backward"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "BK")

        self.token_mock.value = "bk"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "BK")

        self.token_mock.value = "taakse"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "BK")

        self.token_mock.value = "ta"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "BK")

    def test_token_method_returns_rt_identifier_correctly(self):
        self.token_mock.value = "right"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "RT")

        self.token_mock.value = "rt"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "RT")

        self.token_mock.value = "oikealle"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "RT")

        self.token_mock.value = "oi"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "RT")

    def test_token_method_returns_lt_identifier_correctly(self):
        self.token_mock.value = "left"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "LT")

        self.token_mock.value = "lt"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "LT")

        self.token_mock.value = "vasemmalle"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "LT")

        self.token_mock.value = "va"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "LT")

    def test_token_method_returns_stop_identifier_correctly(self):
        self.token_mock.value = "stop"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "STOP")

        self.token_mock.value = "seis"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "STOP")

    def test_token_method_returns_make_identifier_correctly(self):
        self.token_mock.value = "make"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "MAKE")

        self.token_mock.value = "olkoon"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "MAKE")

    def test_token_method_returns_if_identifier_correctly(self):
        self.token_mock.value = "if"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "IF")

        self.token_mock.value = "jos"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "IF")

    def test_token_method_returns_ifelse_identifier_correctly(self):
        self.token_mock.value = "ifelse"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "IFELSE")

        self.token_mock.value = "riippuen"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "IFELSE")

    def test_token_method_returns_for_identifier_correctly(self):
        self.token_mock.value = "for"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "FOR")

        self.token_mock.value = "luvuille"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "FOR")

    def test_token_method_returns_show_identifier_correctly(self):
        self.token_mock.value = "show"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "SHOW")

        self.token_mock.value = "näytä"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "SHOW")

    def test_token_method_returns_true_identifier_correctly(self):
        self.token_mock.value = "true"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "TRUE")

        self.token_mock.value = "joo"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "TRUE")

    def test_token_method_returns_false_identifier_correctly(self):
        self.token_mock.value = "false"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "FALSE")

        self.token_mock.value = "ei"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "FALSE")

    def test_token_method_returns_bye_identifier_correctly(self):
        self.token_mock.value = "bye"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "BYE")

        self.token_mock.value = "heippa"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "BYE")

    def test_token_method_returns_ident_identifier_correctly(self):
        self.token_mock.value = "blahhhhh"
        tok = self.lexer.t_IDENT(self.token_mock)
        self.assertEqual(tok.type, "IDENT")

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

        self.ply_lexer.input(test_string)
        token_abc = self.ply_lexer.token()
        self.assertEqual(token_abc.lineno, 1)
        token_def = self.ply_lexer.token()
        self.assertEqual(token_def.lineno, 3)

    def test_lexer_finds_illegal_characters(self):
        test_string = 'make % "travel.distance 10'

        self.ply_lexer.input(test_string)

        list(self.ply_lexer)

        self.console_mock.write.assert_called()
        self.assertIn("Illegal", self.console_mock.write.call_args.args[0])

    def test_lexer_is_reset_correctly(self):
        self.ply_lexer.lineno = 123
        self.ply_lexer.linestartpos = 45
        self.lexer.reset()
        self.assertNotEqual(self.ply_lexer.lineno, 123)
        self.assertNotEqual(self.ply_lexer.linestartpos, 45)

    def test_identities_cannot_be_only_numbers(self):
        test_string = "to 123 show :x end foo 1 2"

        self.ply_lexer.input(test_string)

        token = self.ply_lexer.token()
        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.NUMBER.value)

    def test_identitities_cannot_have_brackets(self):
        test_string = "to (123 robot.say end foo] 1 2 f{d 50"
        self.ply_lexer.input(test_string)

        for token in self.ply_lexer:
            if token.type == TokenType.IDENT.value:
                self.assertNotEqual(token.value, "(123")
                self.assertNotEqual(token.value, "foo]")
                self.assertNotEqual(token.value, "f{d")

    def test_identities_can_have_numbers(self):
        test_string = "miten 1aliohjelma h1e2i3 end"
        self.ply_lexer.input(test_string)

        for token in self.ply_lexer:
            if token.type == TokenType.IDENT.value:
                self.assertIn(token.value, ["1aliohjelma", "h1e2i3"])

    def test_identities_can_have_scandics(self):
        test_string = "miten röbättå :x robot.say :x end"
        self.ply_lexer.input(test_string)

        token = self.ply_lexer.token()
        token = self.ply_lexer.token()
        self.assertEqual(token.value, "röbättå")

    def test_identities_can_have_periods(self):
        test_string = "12a.2b"
        self.ply_lexer.input(test_string)
        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.IDENT.value)
        self.assertEqual(token.value, "12a.2b")

    def test_identities_cannot_have_operators(self):
        test_string = "miten robotti-mene et 100 end"
        self.ply_lexer.input(test_string)

        for token in self.ply_lexer:
            if token.type == TokenType.IDENT.value:
                self.assertNotEqual(token.value, "robotti-mene")

    def test_identities_cannot_have_spaces(self):
        test_string = "miten robotti mene et 100 end"
        self.ply_lexer.input(test_string)

        for token in self.ply_lexer:
            if token.type == TokenType.IDENT.value:
                self.assertNotEqual(token.value, "robotti mene")

    def test_identities_can_have_non_letters(self):
        test_string = "miten ?r@b#t$! et 100 end"
        self.ply_lexer.input(test_string)

        token = self.ply_lexer.token()
        token = self.ply_lexer.token()
        self.assertEqual(token.value, "?r@b#t$!")

    def test_floats_can_be_written_with_commas_and_periods(self):
        test_string = "123.4 5,678"
        self.ply_lexer.input(test_string)

        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.FLOAT.value)
        self.assertEqual(token.value, 123.4)

        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.FLOAT.value)
        self.assertEqual(token.value, 5.678)

    def test_numbers_and_operators_are_tokenized_correctly_without_spaces(self):
        test_string = "1+2-3/4.5*6"
        self.ply_lexer.input(test_string)

        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.NUMBER.value)
        self.assertEqual(token.value, 1)

        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.PLUS.value)
        self.assertEqual(token.value, "+")

        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.NUMBER.value)
        self.assertEqual(token.value, 2)

        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.MINUS.value)
        self.assertEqual(token.value, "-")

        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.NUMBER.value)
        self.assertEqual(token.value, 3)

        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.DIV.value)
        self.assertEqual(token.value, "/")

        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.FLOAT.value)
        self.assertEqual(token.value, 4.5)

        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.MUL.value)
        self.assertEqual(token.value, "*")

        token = self.ply_lexer.token()
        self.assertEqual(token.type, TokenType.NUMBER.value)
        self.assertEqual(token.value, 6)
