# pylint: disable=invalid-name, too-few-public-methods
"""Parsing rules and globals used by the parser"""

from parser.ast import NodeFactory
from lexer.lexer import Lexer
from utils.logger import Logger
from entities.symbol_table import SymbolTable

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
        self.symbol_table = None
        self.node_factory = None

    def update(self, current_lexer: Lexer, logger: Logger, symbol_table: SymbolTable):
        """Update parser-wide shared fields"""
        self.current_lexer = current_lexer
        self.ply_lexer = current_lexer.get_ply_lexer()
        self.reserved_words = current_lexer.reserved_words
        self.logger = logger
        self.symbol_table = symbol_table
        self.node_factory = NodeFactory(self.logger, self.symbol_table)


shared = Shared()
