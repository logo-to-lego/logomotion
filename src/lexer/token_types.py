"""Token types used by the lexer. """

from enum import Enum


class TokenType(Enum):
    """Insert new token names here and the rule to the Lexer-class."""

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
    IFELSE = "IFELSE"
    SHOW = "SHOW"
    NUMBER = "NUMBER"
    FLOAT = "FLOAT"
    TRUE = "TRUE"
    FALSE = "FALSE"
    BYE = "BYE"
