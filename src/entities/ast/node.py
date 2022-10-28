# pylint: disable=missing-class-docstring,missing-function-docstring, unused-argument, too-many-instance-attributes
""" Abstract Syntax Tree node definitions, returned by the parser. """
from entities.logotypes import LogoType
from entities.symbol_tables import SymbolTables, default_symbol_tables
from utils.code_generator import default_code_generator
from utils.logger import Logger, default_logger


class Node:
    """Base AST Node class"""


    def __init__(self, node_type, children=None, leaf=None, **dependencies):
        self.type = node_type
        self.children = children if children else []
        self.leaf = leaf
        self._logger: Logger = dependencies.get("logger", default_logger)
        self._symbol_tables: SymbolTables = dependencies.get("symbol_tables", default_symbol_tables)
        self.position = dependencies.get("position", None)
        self._logo_type = None
        self._code_generator = dependencies.get("code_generator", default_code_generator)

    def get_type(self) -> LogoType:
        return self._logo_type

    def set_type(self, new_type: LogoType):
        self._logo_type = new_type

    def __str__(self):
        result = f"({self.type}"

        if self.leaf:
            result += f", {self.leaf if self.leaf else 'None'}"

        if self._logo_type:
            result += f", logo type: {self._logo_type.value}"

        if self.children:
            result += ", children: ["
            result += ", ".join((child.__str__() for child in self.children))
            result += "]"

        result += ")"

        return result

    def undefined_variables(self):
        """Checks if the current scope has undefined variables
        and returns a list of them.
        """
        undefined = []
        for symbol in self._symbol_tables.variables.get_current_scope().values():
            if symbol.type is LogoType.UNKNOWN:
                undefined.append(symbol.name)
        return undefined

    def generate_code(self):
        """Calls generate_code recursively on all child nodes."""
        for child in self.children:
            child.generate_code()

    def generate_temp_var(self):
        Node.TEMP_VAR_INDEX += 1
        return f"temp{Node.TEMP_VAR_INDEX}"


class Start(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("Start", children, **dependencies)

    def check_types(self):
        """Runs semantic analysis on the AST nodes to find type errors, undefined
        functions/variables and to figure out implied typing."""
        for child in self.children:
            child.check_types()


class NodeFactory:
    """Used to create new AST nodes, injects logger and symbol table as dependencies."""

    def __init__(
        self,
        logger=default_logger,
        symbol_tables=default_symbol_tables,
        code_generator=default_code_generator,
    ):

        self._logger = logger
        self._symbol_tables = symbol_tables
        self._code_generator = code_generator

    def create_node(self, node_class: Node, **kwargs):
        """Creates a new node of node_class, with the given keyword arguments."""
        return node_class(
            **kwargs,
            logger=self._logger,
            symbol_tables=self._symbol_tables,
            code_generator=self._code_generator,
        )
