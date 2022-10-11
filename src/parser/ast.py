# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods
""" Abstract Syntax Tree node definitions, returned by the parser. """
from entities.symbol_table import default_symbol_table


class Node:
    def __init__(self, node_type, children=None, leaf=None):
        self.type = node_type
        self.children = children if children else []
        self.leaf = leaf
        self.symbol_table = default_symbol_table

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
    def __init__(self, children=None):
        super().__init__("Start", children)


class StatementList(Node):
    def __init__(self, children=None):
        super().__init__("StatementList", children, None)


class Statement(Node):
    def __init__(self, children=None):
        super().__init__("Statement", children, None)


class Command(Node):
    pass


class BinOp(Node):
    def __init__(self, children, leaf):
        super().__init__("BinOp", children, leaf)


class UnaryOp(Node):
    def __init__(self, children, leaf):
        super().__init__("UnaryOp", children, leaf)


class RelOp(Node):
    def __init__(self, children, leaf):
        super().__init__("RelOp", children, leaf)


class Number(Node):
    def __init__(self, leaf):
        super().__init__("Number", children=None, leaf=leaf)


class Float(Node):
    def __init__(self, leaf):
        super().__init__("Float", children=None, leaf=leaf)


class Bool(Node):
    def __init__(self, leaf):
        super().__init__("Bool", children=None, leaf=leaf)


class Identifier(Node):
    def __init__(self, leaf):
        super().__init__("Ident", children=None, leaf=leaf)


class Deref(Node):
    def __init__(self, leaf):
        super().__init__("Deref", children=None, leaf=leaf)


class StringLiteral(Node):
    def __init__(self, leaf):
        super().__init__("StringLiteral", children=None, leaf=leaf)


class If(Node):
    def __init__(self, children, leaf):
        super().__init__("If", children, leaf)


class IfElse(Node):
    def __init__(self, children, leaf):
        super().__init__("IfElse", children, leaf)


class ProcDecl(Node):
    def __init__(self, children, leaf):
        super().__init__("ProcDecl", children, leaf)


class ProcArgs(Node):
    def __init__(self, children=None):
        super().__init__("ProcArgs", children)
