# pylint: disable=too-few-public-methods
"""The evaluation module of the analysis part"""

from parser.ast import Node
from entities.symbol_table import SymbolTable

class Evaluation:
    """The Evaluation class houses methods for semantic analysis for the nodes in the AST.
    Attributes:
        semantic_checks: A dictionary containing the semantic check methods
        semantic_errors: A list containing discovered semantic errors
        symbol_table: The symbol table to use for symbol lookups"""

    def __init__(self, symbol_table: SymbolTable):
        """Initialize a new Evaluation object
        Args:
            symbol_table: The symbol table to use for symbol lookups."""

        self.semantic_checks = {
            "SA_SYMBOL_EXISTS": self.symbol_exists_routine,
        }
        self.semantic_errors = []
        self.symbol_table = symbol_table

    def symbol_exists_routine(self, node: Node):
        """Check if a symbol exists within the current scope.
        Args:
            node: The Deref node to check
        Returns: True if the symbol exists in the current scope, False if not"""

        if node.type != "Deref":
            raise Exception("ASTNodeMismatch",
                            f"Method expected Deref node and instead got {node.type}")

        symbol_type = self.symbol_table.lookup(node.leaf)
        if not symbol_type:
            # Should likely make a separate class for error messages for easier localization?
            self.semantic_errors.append(f"Not Initialized Error: What is '{node.leaf}'?")
            return False

        return True
