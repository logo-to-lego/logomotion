# pylint: disable=missing-class-docstring,missing-function-docstring,
""" Abstract Syntax Tree node definitions, returned by the parser. """
from entities.symbol_table import default_symbol_table
from utils.logger import default_logger


class Node:
    def __init__(self, node_type, children=None, leaf=None, **dependencies):
        self.type = node_type
        self.children = children if children else []
        self.leaf = leaf
        self._logger = dependencies.get("logger", default_logger)
        self._symbol_table = dependencies.get("symbol_table", default_symbol_table)

    def __str__(self):
        result = f"({self.type}"

        if self.leaf:
            result += f", {self.leaf if self.leaf else 'None'}"

        if self.children:
            result += ", children: ["
            result += ", ".join((child.__str__() for child in self.children))
            result += "]"

        result += ")"

        return result


class Start(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("Start", children, **dependencies)


class StatementList(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("StatementList", children, None, **dependencies)


class Statement(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("Statement", children, None, **dependencies)


class Command(Node):
    pass


class BinOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("BinOp", children, leaf, **dependencies)


class UnaryOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("UnaryOp", children, leaf, **dependencies)


class RelOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("RelOp", children, leaf, **dependencies)


class Number(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Number", children=None, leaf=leaf, **dependencies)


class Float(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Float", children=None, leaf=leaf, **dependencies)


class Bool(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Bool", children=None, leaf=leaf, **dependencies)


class Identifier(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Ident", children=None, leaf=leaf, **dependencies)


class Deref(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Deref", children=None, leaf=leaf, **dependencies)


class StringLiteral(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("StringLiteral", children=None, leaf=leaf, **dependencies)


class If(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("If", children, leaf, **dependencies)


class IfElse(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("IfElse", children, leaf, **dependencies)


class ProcDecl(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("ProcDecl", children, leaf, **dependencies)


class ProcArgs(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("ProcArgs", children, **dependencies)


class NodeFactory:
    def __init__(self, logger=default_logger, symbol_table=default_symbol_table):
        self._logger = logger
        self._symbol_table = symbol_table

    def create_node(self, node_class: Node, **kwargs):
        return node_class(**kwargs, logger=self._logger, symbol_table=self._symbol_table)
