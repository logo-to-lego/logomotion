# pylint: disable=invalid-name, too-few-public-methods
"""Parsing rules and globals used by the parser"""

from lexer.lexer import Lexer

precedence = (
    ("nonassoc", "EQUALS", "LESSTHAN", "GREATERTHAN", "LTEQUALS", "GTEQUALS"),
    ("left", "PLUS", "MINUS"),
    ("left", "MUL", "DIV"),
    ("right", "UMINUS"),
)


names = {}

start = "start"


class LexerWrapper:
    """Wrapper class for exposing the lexer to parser functions."""

    def __init__(self) -> None:
        self.reserved_words = {}
        self.ply = None
        self.current_lexer = None

    def update(self, current_lexer: Lexer):
        """Update wrapper fields with current_lexer."""
        self.current_lexer = current_lexer
        self.ply = current_lexer.get_ply_lexer()
        self.reserved_words = current_lexer.reserved_words


lexer = LexerWrapper()
