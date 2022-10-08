# pylint: disable=invalid-name, too-few-public-methods
"""Parsing rules and globals used by the parser"""

from lexer.lexer import Lexer
from utils.logger import Logger

precedence = (
    ("nonassoc", "EQUALS", "LESSTHAN", "GREATERTHAN", "LTEQUALS", "GTEQUALS"),
    ("left", "PLUS", "MINUS"),
    ("left", "MUL", "DIV"),
    ("right", "UMINUS"),
)


names = {}

start = "start"


class Shared:
    """Wrapper class for exposing the lexer, console_io,
    symbol tables, error_handler to parser functions."""

    def __init__(self) -> None:
        self.reserved_words = {}
        self.ply_lexer = None
        self.current_lexer = None
        self.logger = None

    def update(self, current_lexer: Lexer, logger: Logger):
        """Update parser-wide shared fields"""
        self.current_lexer = current_lexer
        self.ply_lexer = current_lexer.get_ply_lexer()
        self.reserved_words = current_lexer.reserved_words
        self.logger = logger


shared = Shared()
