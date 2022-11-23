# pylint: disable=invalid-name, too-few-public-methods
"""Parsing rules and globals used by the parser"""

from lexer.lexer import Lexer
from utils.code_generator import JavaCodeGenerator
from utils.logger import Logger
from entities.symbol_tables import SymbolTables
from entities.ast.node import NodeFactory

precedence = (
    ("nonassoc", "EQUALS", "LESSTHAN", "GREATERTHAN", "LTEQUALS", "GTEQUALS"),
    ("left", "PLUS", "MINUS"),
    ("left", "MUL", "DIV"),
    ("right", "UMINUS"),
)


names = {}

start = "start"


class Position:
    "Stores position data for a production symbol."

    def __init__(self, prod):
        self._linespan = prod.linespan(0)
        self._lexspan = prod.lexspan(0)
        self._linestartpos = shared.ply_lexer.linestartpos

    def get_pos(self):
        "Returns a tuple (linepos, colpos)."
        line = self._linespan[0]
        col = self._lexspan[0] - self._linestartpos

        return (line, col)

    def get_lexspan(self):
        return self._lexspan


class Shared:
    """Wrapper class for exposing the lexer, console_io,
    symbol tables, error_handler to parser functions."""

    def __init__(self) -> None:
        self.reserved_words = {}
        self.ply_lexer = None
        self.current_lexer = None
        self.logger = None
        self.symbol_tables = None
        self.node_factory = None
        self.code_generator = None

    def update(
        self,
        current_lexer: Lexer,
        logger: Logger,
        symbol_tables: SymbolTables,
        code_generator: JavaCodeGenerator,
    ):
        """Update parser-wide shared fields"""
        self.current_lexer = current_lexer
        self.ply_lexer = current_lexer.get_ply_lexer()
        self.reserved_words = current_lexer.reserved_words
        self.logger = logger
        self.symbol_tables = symbol_tables
        self.code_generator = code_generator
        self.node_factory = NodeFactory(self.logger, self.symbol_tables, self.code_generator)


shared = Shared()
