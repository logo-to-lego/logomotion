"""
Lexer module used by PLY's lexer-generator.
"""
# pylint: disable=missing-function-docstring, invalid-name

from ply.lex import lex, TOKEN
from lexer.token_types import TokenType
from utils.logger import default_logger
from utils.lowercase_converter import convert_to_lowercase as to_lowercase


class Lexer:
    """Lexer using PLY for tokenizing an input stream."""

    # Maps <keyword in input> to <token type>
    reserved_words = {
        "to": TokenType.TO,
        "miten": TokenType.TO,
        "end": TokenType.END,
        "valmis": TokenType.END,
        "output": TokenType.OUTPUT,
        "anna": TokenType.OUTPUT,
        "op": TokenType.OUTPUT,
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
        "repeat": TokenType.REPEAT,
        "toista": TokenType.REPEAT,
        "show": TokenType.SHOW,
        "tulosta": TokenType.SHOW,
        "true": TokenType.TRUE,
        "joo": TokenType.TRUE,
        "false": TokenType.FALSE,
        "ei": TokenType.FALSE,
        "bye": TokenType.BYE,
        "heippa": TokenType.BYE,
    }

    OPERATORS = r"+\-\/\*\<\>\=\<>"
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
        TokenType.NOTEQUALS: r"\<>",
        TokenType.LESSTHAN: r"\<",
        TokenType.GREATERTHAN: r"\>",
        TokenType.LTEQUALS: r"\<\=",
        TokenType.GTEQUALS: r"\>\=",
        TokenType.STRINGLITERAL: r"[\"\']" + VARIABLE_NAME,
        TokenType.DEREF: r"\:" + VARIABLE_NAME,
        TokenType.COMMA: r",",
    }

    def __init__(self, logger=default_logger):
        self._ply_lexer = None
        self.tokens = []
        self._init_tokens()
        self._procedure_tokens = {}
        self._expect_procedure_name_as_ident = False
        self._logger = logger

        # Set regex only tokens.
        for name, value in self.token_types.items():
            setattr(self, "t_" + name.value, value)

    def _init_tokens(self):
        "Resets the tokens list to initial values."
        self.tokens.clear()
        self.tokens.extend([token_type.value for token_type in TokenType])

    # Token methods. Name as t_<TOKEN_NAME>, where TOKEN_NAME is in the tokens-list.
    # Declaration order matters for matching, i.e. longest similar regex first.

    @TOKEN(FUNCTION_NAME)
    def t_IDENT(self, token):
        """Used for tokenizing all identifiers, keywords."""
        word = to_lowercase(token.value)
        token.value = word
        token.type = self.reserved_words.get(word, TokenType.IDENT).value

        # Check if the token value is a user defined procedure
        if token.type == TokenType.IDENT.value and token.value in self._procedure_tokens:
            if not self._expect_procedure_name_as_ident:
                # Change token type to that of the mapped token value for this procedure
                # when the token appears outside of the TO IDENT - procedure declaration
                # context.
                token.type = self._procedure_tokens[token.value]

        self._expect_procedure_name_as_ident = False

        if token.type == TokenType.TO.value:
            # Update state to be inside a TO IDENT - context.
            self._expect_procedure_name_as_ident = True

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
        self._logger.debug(f"Illegal char {token.value[0]!r}")
        self._logger.error_handler.add_error(
            "unknown_character",
            lexspan=(token.lexpos, token.lexpos),
            char=token.value[0]
        )
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

    def get_procedure_tokens(self):
        """Returns a dict of procedure name, token name pairs. Used to map a user defined
        procedure to lexer token names."""
        return self._procedure_tokens

    def add_procedure_token(self, procedure_name, token_name):
        "Adds a new procedure token to the lexer."
        self._procedure_tokens[procedure_name] = token_name
        self.tokens.append(token_name)

    def get_tokens(self):
        "Returns a list of lexer tokens for the parser."
        return self.tokens

    def reset(self):
        """Resets the lexer's internal state."""
        if not self._ply_lexer:
            self.build()

        self._ply_lexer.lineno = 1  # Must reset here, since it isn't done by PLY.
        self._ply_lexer.linestartpos = 0

        # Each parse can add new tokens, so we clear these
        self._init_tokens()
        self._procedure_tokens.clear()
        self._expect_procedure_name_as_ident = False

    def tokenize_input(self, code):
        """Turns input code into a list of tokens."""
        if not self._ply_lexer:
            self.build()
        self.reset()

        self._ply_lexer.input(code)
        tokens = list(self._ply_lexer)

        self.reset()
        return tokens
