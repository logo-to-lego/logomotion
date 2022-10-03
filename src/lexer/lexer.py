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
        "ifelse": TokenType.IFELSE,
        "riippuen": TokenType.IFELSE,
        "for": TokenType.FOR,
        "luvuille": TokenType.FOR,
        "show": TokenType.SHOW,
        "näytä": TokenType.SHOW,
        "true": TokenType.TRUE,
        "joo": TokenType.TRUE,
        "false": TokenType.FALSE,
        "ei": TokenType.FALSE,
        "bye": TokenType.BYE,
        "heippa": TokenType.BYE,
    }

    OPERATORS = r"+\-\/\*\<\>\="
    BRACKETS = r"\[\]\(\)\{\}"
    FORBIDDEN_CHARS = r" \"\'\:\;\n\r" + OPERATORS + BRACKETS

    FUNCTION_NAME = r"[^" + FORBIDDEN_CHARS + r"]*[a-zA-ZåäöÅÄÖ][^" + FORBIDDEN_CHARS + r"]*"
    VARIABLE_NAME = r"[^" + FORBIDDEN_CHARS + "]+"

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
        TokenType.LESSTHAN: r"\<",
        TokenType.GREATERTHAN: r"\>",
        TokenType.LTEQUALS: r"\<\=",
        TokenType.GTEQUALS: r"\>\=",
        TokenType.STRINGLITERAL: r"[\"\']" + VARIABLE_NAME,
        TokenType.DEREF: r"\:" + VARIABLE_NAME,
        TokenType.COMMA: r",",
    }

    def __init__(self, console_io=default_console_io):
        self._ply_lexer = None
        self.tokens = [token_type.value for token_type in TokenType]
        self.console_io = console_io

        # Set regex only tokens.
        for name, value in self.token_types.items():
            setattr(self, "t_" + name.value, value)

    # Token methods. Name as t_<TOKEN_NAME>, where TOKEN_NAME is in the tokens-list.
    # Declaration order matters for matching, i.e. longest similar regex first.

    @TOKEN(FUNCTION_NAME)
    def t_IDENT(self, token):
        """Used for tokenizing all identifiers, keywords."""
        word = token.value.lower()
        token.type = self.reserved_words.get(word, TokenType.IDENT).value
        return token

    @TOKEN(r"\d+[\.\,]\d+")
    def t_FLOAT(self, token):
        values = token.value.split(",")
        if len(values) == 2:
            token.value = f"{values[0]}" + "." + f"{values[1]}"
        token.value = float(token.value)
        return token

    @TOKEN(r"\d+")
    def t_NUMBER(self, token):
        token.value = float(token.value)
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
        self._ply_lexer = lex(object=self, **kwargs)
        self.reset()

    def get_ply_lexer(self):
        """Returns the built ply lexer."""
        if not self._ply_lexer:
            self.build()

        return self._ply_lexer

    def reset(self):
        """Resets the lexer's internal state."""
        if not self._ply_lexer:
            self.build()

        self._ply_lexer.lineno = 1  # Must reset here, since it isn't done by PLY.
        self._ply_lexer.linestartpos = 0

    def tokenize_input(self, code):
        """Turns input code into a list of tokens."""
        self.build()
        self.reset()

        self._ply_lexer.input(code)
        tokens = list(self._ply_lexer)

        self.reset()
        return tokens
