"""
Lexer module used by PLY's lexer-generator.
"""
# pylint: disable=missing-function-docstring, invalid-name

from ply.lex import lex, TOKEN
from lexer.token_types import TokenType, token_types, reserved_words, NAME_REGEX
from utils.console_io import ConsoleIO


class Lexer:
    """Lexer using PLY for tokenizing an input stream."""

    def __init__(self):
        self.lexer = None
        self.tokens = [token_type.value for token_type in TokenType]

        # Set regex only tokens.
        for name, value in token_types.items():
            setattr(self, "t_" + name.value, value)

    # Token methods. Name as t_<TOKEN_NAME>, where TOKEN_NAME is in the tokens-tuple.

    @TOKEN(r"\d+")
    def t_NUMBER(self, token):
        token.value = int(token.value)
        return token

    @TOKEN(NAME_REGEX)
    def t_IDENT(self, token):
        """Used for tokenizing all identifiers, keywords"""
        token.type = reserved_words.get(token.value, "IDENT")
        return token

    # Ignored tokens, do not put these in the tokens-tuple.

    t_ignore = r" \t"

    @TOKEN(r"(\r?\n)+")
    def t_ignore_newline(self, token):
        token.lexer.lineno += token.value.count("\n")

    @TOKEN(r"\;.*\n")
    def t_ignore_comment(self, token):
        token.lexer.lineno += 1

    def t_error(self, token):
        ConsoleIO.write(f"Illegal char {token.value[0]!r}")
        token.lexer.skip(1)

    def build(self, **kwargs):
        """Builds the lexer based on token rules."""
        self.lexer = lex(object=self, **kwargs)

    def get_lexer(self):
        """Returns created ply lexer. Call only after calling build."""
        return self.lexer
