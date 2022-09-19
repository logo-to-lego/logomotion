"""
Lexer module used by PLY's lexer-generator.
"""
# pylint: disable=missing-function-docstring, invalid-name

from ply.lex import lex, TOKEN
from lexer.token_types import TokenType
from utils.console_io import default_console_io


class Lexer:
    """Lexer using PLY for tokenizing an input stream."""

    # Maps <keyword in input> to <token type>
    reserved_words = {
        "to": TokenType.TO,
        "miten": TokenType.TO,
        "end": TokenType.END,
        "valmis": TokenType.END,
        "fd": TokenType.FD,
        "forward": TokenType.FD,
        "et": TokenType.FD,
        "eteen": TokenType.FD,
        "bk": TokenType.BK,
        "backward": TokenType.BK,
        "ta": TokenType.BK,
        "taakse": TokenType.BK,
        "rt": TokenType.RT,
        "right": TokenType.RT,
        "oi": TokenType.RT,
        "oikealle": TokenType.RT,
        "lt": TokenType.LT,
        "left": TokenType.LT,
        "va": TokenType.LT,
        "vasemmalle": TokenType.LT,
        "stop": TokenType.STOP,
        "seis": TokenType.STOP,
        "make": TokenType.MAKE,
        "olkoon": TokenType.MAKE,
        "if": TokenType.IF,
        "jos": TokenType.IF,
        "for": TokenType.FOR,
        "luvuille": TokenType.FOR,
        "show": TokenType.SHOW,
        "näytä": TokenType.SHOW,
    }

    NAME_REGEX = r"[\w_][\w\d_.]*"

    # Add tokens with only regex rules here.
    # If the token needs a function call, add it only as a method.
    # Do not use regex like 'foo' here, add them to reserved_words.
    token_types = {
        TokenType.MUL: r"\*",
        TokenType.DIV: r"\/",
        TokenType.PLUS: r"\+",
        TokenType.MINUS: r"\-",
        TokenType.LPAREN: r"\(",
        TokenType.RPAREN: r"\)",
        TokenType.LBRACKET: r"\[",
        TokenType.RBRACKET: r"\]",
        TokenType.LBRACE: r"\{",
        TokenType.RBRACE: r"\}",
        TokenType.EQUALS: r"\=",
        TokenType.STRINGLITERAL: r"\"" + NAME_REGEX,
        TokenType.DEREF: r"\:" + NAME_REGEX,
        TokenType.COMMA: r",",
    }

    def __init__(self, console_io=default_console_io):
        self.lexer = None
        self.tokens = [token_type.value for token_type in TokenType]
        self.console_io = console_io

        # Set regex only tokens.
        for name, value in self.token_types.items():
            setattr(self, "t_" + name.value, value)

    # Token methods. Name as t_<TOKEN_NAME>, where TOKEN_NAME is in the tokens-list.

    @TOKEN(r"\d+")
    def t_NUMBER(self, token):
        token.value = int(token.value)
        return token

    @TOKEN(NAME_REGEX)
    def t_IDENT(self, token):
        """Used for tokenizing all identifiers, keywords."""
        token.type = self.reserved_words.get(token.value, TokenType.IDENT).value
        return token

    # Ignored tokens, do not put these in the tokens-list.

    t_ignore = " \t"

    @TOKEN(r"(\r?\n)+")
    def t_ignore_newline(self, token):
        token.lexer.lineno += token.value.count("\n")
        token.lexer.linestartpos = token.lexpos + 1

    @TOKEN(r"\;.*")
    def t_ignore_comment(self, token):
        pass

    def t_error(self, token):
        self.console_io.write(f"Illegal char {token.value[0]!r}")
        token.lexer.skip(1)

    def build(self, **kwargs):
        """Builds the lexer based on token rules."""
        self.lexer = lex(object=self, **kwargs)
        self.lexer.linestartpos = 0

    def get_lexer(self):
        """Returns the ply lexer."""
        if not self.lexer:
            self.build()

        return self.lexer
