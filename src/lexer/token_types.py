"""Define token types.

Token types are used by PLY's lexer-generator to make the lexer. Input stream
is split into a stream of tokens according to regex/rules defined here.
"""

from enum import Enum

NAME_REGEX = r"[\w_][\w\d_.]*"


class TokenType(Enum):
    """Insert new token names here and the related regex/rule to the dict below."""

    IDENT = "IDENT"
    MUL = "MUL"
    DIV = "DIV"
    PLUS = "PLUS"
    MINUS = "MINUS"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    EQUALS = "EQUALS"
    STRINGLITERAL = "STRINGLITERAL"
    DEREF = "DEREF"
    TO = "TO"
    END = "END"
    COMMA = "COMMA"
    FD = "FD"
    BK = "BK"
    RT = "RT"
    LT = "LT"
    STOP = "STOP"
    MAKE = "MAKE"
    FOR = "FOR"
    IF = "IF"
    NUMBER = "NUMBER"


# Add tokens with only regex rules here.
# If the token needs a function call, add it in the lexer.
# Do not use regex like 'foo' here, add it to the reserved dict and
# handle it in t_IDENT of the lexer.
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

# Maps <word in input> to <token type string>
reserved_words = {
    "to": TokenType.TO.value,
    "end": TokenType.END.value,
    "fd": TokenType.FD.value,
    "forward": TokenType.FD.value,
    "bk": TokenType.BK.value,
    "backward": TokenType.BK.value,
    "rt": TokenType.RT.value,
    "right": TokenType.RT.value,
    "lt": TokenType.LT.value,
    "left": TokenType.LT.value,
    "stop": TokenType.STOP.value,
    "make": TokenType.MAKE.value,
    "if": TokenType.IF.value,
    "for": TokenType.FOR.value,
}
