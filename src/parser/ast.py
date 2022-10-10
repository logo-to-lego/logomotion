# pylint: disable=missing-class-docstring,missing-function-docstring, unused-argument
""" Abstract Syntax Tree node definitions, returned by the parser. """
from entities.logotypes import LogoType
from entities.symbol import Variable
from entities.symbol_tables import SymbolTables, default_symbol_tables
from lexer.token_types import TokenType
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


class Start(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("Start", children, **dependencies)

    def check_types(self):
        """Runs semantic analysis on the AST nodes to find type errors, undefined
        functions/variables and to figure out implied typing."""
        for child in self.children:
            child.check_types()


class StatementList(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("StatementList", children, None, **dependencies)

    def check_types(self):
        """Runs the check in given order."""
        for child in self.children:
            child.get_type()
            child.check_types()


class Command(Node):
    def __init__(self, node_type, children=None, leaf=None, **dependencies):
        super().__init__(node_type, children, leaf, **dependencies)
        self._type_checkers = {
            TokenType.FD: self._check_fd_types,
            TokenType.MAKE: self._check_make_types,
        }
        self._type_getters = {TokenType.FD: self._get_fd_type, TokenType.MAKE: self._get_make_type}

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.UNKNOWN

        return self._type_getters.get(self.type, lambda: self._logo_type)()

    def _get_fd_type(self):
        self._logo_type = LogoType.VOID
        return self._logo_type

    def _check_fd_types(self):
        if len(self.children) != 1:
            self._logger.console.write("Wrong amount of arguments for FD")
            return

        child = self.children[0]
        child_type = child.get_type()
        if child_type == LogoType.UNKNOWN:
            child.set_type(LogoType.FLOAT)
        elif child_type != LogoType.FLOAT:
            self._logger.console.write("Type should be float, not " + child.get_type().value)
        child.check_types()

    def _get_make_type(self):
        self._logo_type = LogoType.VOID
        return self._logo_type

    def _check_make_types(self):
        if len(self.children) != 1 or not self.leaf:
            self._logger.console.write("Wrong amount of arguments for MAKE")
            return

        # Check first argument type, variable name
        name = self.leaf
        name_type = name.get_type()

        if name_type == LogoType.UNKNOWN:
            name.set_type(LogoType.STRING)
        elif name.get_type() != LogoType.STRING:
            self._logger.console.write(
                "Type should be string literal, not " + name.get_type().value
            )
        name.check_types()

        # Check second argument type, assignment value
        value = self.children[0]
        value_type = value.get_type()

        if value_type == LogoType.VOID:
            self._logger.console.write("Type should not be VOID")
        value.check_types()

        if name.get_type() == LogoType.STRING:
            symbol = self._symbol_tables.variables.lookup(name.leaf)
            if symbol:
                if symbol.type == LogoType.UNKNOWN:
                    symbol.type = value.get_type()
                elif value.get_type() == LogoType.UNKNOWN:
                    value.set_type(symbol.type)
                elif value.get_type() != symbol.type:
                    self._logger.console.write(
                        f"Variable type cannot be changed, was {symbol.type.value}"
                        + f", trying to change to {value.get_type().value}"
                    )
            else:
                symbol = Variable(name.leaf, value.get_type())
                self._symbol_tables.variables.insert(name.leaf, symbol)

    def check_types(self):
        """Checks that the args given to the procedure are of correct type and that there are
        only as many arguments as the procedure takes in."""
        checker = self._type_checkers.get(
            self.type,
            lambda: self._logger.console.write("No type checker found for " + self.type.value),
        )
        checker()


class BinOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("BinOp", children, leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.FLOAT

        return self._logo_type

    def check_types(self):
        """Checks that the types of both operands is LogoFloat"""
        for child in self.children:
            child_type = child.get_type()
            if child_type == LogoType.UNKNOWN:
                child.set_type(LogoType.FLOAT)
            elif child_type != LogoType.FLOAT:
                pos = child.position.get_pos()
                self._logger.error_handler.add_error(2002, row=pos[0])
            child.check_types()


class UnaryOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("UnaryOp", children, leaf, **dependencies)


class RelOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("RelOp", children, leaf, **dependencies)


class Float(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Float", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.FLOAT

        return self._logo_type

    def check_types(self):
        pass


class Bool(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Bool", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.BOOL

        return self._logo_type

    def check_types(self):
        pass


class Deref(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Deref", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.UNKNOWN

        symbol = self._get_symbol()

        if symbol:
            self._logo_type = symbol.type

        return self._logo_type

    def set_type(self, new_type: LogoType):
        self._logo_type = new_type

        symbol = self._get_symbol()

        if symbol and symbol.type == LogoType.UNKNOWN:
            symbol.type = new_type

    def _get_symbol(self) -> Variable:
        return self._symbol_tables.variables.lookup(self.leaf)

    def check_types(self):
        symbol = self._get_symbol()

        if not symbol:
            self._logger.console.write(f"No such variable: {self.leaf}")
        elif symbol.type != self._logo_type:
            self._logger.console.write(
                f"Wrong variable type, was {symbol.type.value} in table "
                + f"but expected {self._logo_type.value}"
            )


class StringLiteral(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("StringLiteral", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.STRING

        return self._logo_type

    def check_types(self):
        pass


class If(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("If", children, leaf, **dependencies)

    def get_type(self):
        return None

    def check_types(self, reverse=False):
        if self.leaf.get_type() is not LogoType.BOOL:
            self._logger.debug("If statements leafs type isn't boolean")
            #self._logger.error_handler.write_errors_to_console() # type error
        self.leaf.check_types()
        self._symbol_tables.variables.initialize_scope()
        self.children[0].check_types()
        self._symbol_tables.variables.finalize_scope()


class IfElse(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("IfElse", children, leaf, **dependencies)

    def get_type(self):
        return None

    def check_types(self, reverse=False):
        if self.leaf.get_type() is not LogoType.BOOL:
            self._logger.debug("IfElse statements leafs type isn't boolean")
            #self._logger.error_handler.write_errors_to_console() # type error
        self.leaf.check_types()
        self._symbol_tables.variables.initialize_scope()
        for child in self.children:
            child.check_types()
        self._symbol_tables.variables.finalize_scope()


class ProcDecl(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("ProcDecl", children, leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.UNKNOWN

        return self._logo_type

    def check_types(self):
        if self._symbol_tables.functions.lookup(self.leaf):
            self._logger.console.write(f"Procedure {self.leaf} already declared")


class ProcArgs(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("ProcArgs", children, **dependencies)


class NodeFactory:
    """Used to create new AST nodes, injects logger and symbol table as dependencies."""

    def __init__(self, logger=default_logger, symbol_tables=default_symbol_tables):
        self._logger = logger
        self._symbol_tables = symbol_tables

    def create_node(self, node_class: Node, **kwargs):
        """Creates a new node of node_class, with the given keyword arguments."""
        return node_class(**kwargs, logger=self._logger, symbol_tables=self._symbol_tables)
