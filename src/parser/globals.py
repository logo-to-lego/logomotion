# pylint: disable=invalid-name, too-few-public-methods
"""Parsing rules and globals used by the parser"""

from lexer.lexer import Lexer
from utils.console_io import ConsoleIO
from entities.error_handler import ErrorHandler

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
        self.console = None
        self.error_handler = None

    def update(self, current_lexer: Lexer, console_io: ConsoleIO, error_handler: ErrorHandler):
        """Update parser-wide shared fields"""
        self.current_lexer = current_lexer
        self.ply_lexer = current_lexer.get_ply_lexer()
        self.reserved_words = current_lexer.reserved_words
        self.console = console_io
        self.error_handler = error_handler


shared = Shared()
