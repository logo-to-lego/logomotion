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
        self.token_mock.lexer.linestartpos = 0
        self.token_mock.lexpos = 0

    def tearDown(self):
        self.token_mock = Mock()

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

        lexer = self.lexer.get_ply_lexer()
        lexer.input(test_string)
        token_abc = lexer.token()
        self.assertEqual(token_abc.lineno, 1)
        token_def = lexer.token()
        self.assertEqual(token_def.lineno, 3)

    def test_lexer_finds_illegal_characters(self):
        test_string = 'make % "travel.distance 10'

        lexer = self.lexer.get_ply_lexer()
        lexer.input(test_string)

        for token in lexer:
            pass

        self.console_mock.write.assert_called()
        self.assertIn("Illegal", self.console_mock.write.call_args.args[0])
