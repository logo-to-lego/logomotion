# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods
""" Abstract Syntax Tree node definitions, returned by the parser. """
from entities.error_values import ErrorValues
from entities.error_info import ErrorInfo
from entities.symbol_table import default_symbol_table
from lexer.token_types import TokenType


class Node:
    def __init__(self, node_type, children=None, leaf=None):
        self.type = node_type
        self.children = children if children else []
        self.leaf = leaf
        self.value = None
        self.symbol_table = default_symbol_table

    def __str__(self):
        result = f"({self.type}"

        if self.leaf:
            result += f", {self.leaf if self.leaf else 'None'}"

        if self.value is not None:
            result += f", value: {self.value}"

        if self.children:
            result += ", children: ["
            result += ", ".join((child.__str__() for child in self.children))
            result += "]"

        result += ")"

        return result

    def check_for_errs(self, children=None, err_msg=""):
        """check for errorvalues, if doesnt exist, create one"""
        errs = []
        if not children:
            children = []
        for child in children:
            if isinstance(child.value, ErrorValues):
                errs += child.value.errors
        err_val = ErrorValues()
        if err_msg:
            err_info = ErrorInfo(self, err_msg)
            err_val.add_error(err_info)
        err_val.errors = errs
        return err_val


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

    def eval(self):
        # Tämän hetkisessä versiossa tyypit oletetaan sopiviksi
        # Esim. int + int, EI string + int. Tarkemmat ohjeet
        # def Equals funktiossa
        for child in self.children:
            if type(child.value) not in (int, float, ErrorValues):
                self.value = self.check_for_errs(
                    self.children, "virhe: binop muksu muu kuin int tai float"
                )
                return
            if isinstance(child.value, ErrorValues):
                self.value = self.check_for_errs(self.children)
                return
        if self.leaf == "+":
            self.value = self.children[0].value + self.children[1].value
        elif self.leaf == "-":
            self.value = self.children[0].value - self.children[1].value
        elif self.leaf == "*":
            self.value = self.children[0].value * self.children[1].value
        elif self.leaf == "/":
            self.value = self.children[0].value / self.children[1].value
        else:
            self.value = self.value = self.check_for_errs(self.children, "virhe: tuntematon binop")


class UnaryOp(Node):
    def __init__(self, children, leaf):
        super().__init__("UnaryOp", children, leaf)

    def eval(self):
        # pitää ehkä tarkistaa, että muksu on float, int, error tai bool
        if isinstance(self.children[0].value, ErrorValues):
            self.value = self.check_for_errs(self.children)
        else:
            self.value = -self.children[0].value


class RelOp(Node):
    def __init__(self, children, leaf):
        super().__init__("RelOp", children, leaf)


class Number(Node):
    def __init__(self, leaf):
        super().__init__("Number", children=None, leaf=leaf)

    def eval(self):
        self.value = self.leaf


class Float(Node):
    def __init__(self, leaf):
        super().__init__("Float", children=None, leaf=leaf)

    def eval(self):
        self.value = self.leaf


class Bool(Node):
    def __init__(self, leaf):
        super().__init__("Bool", children=None, leaf=leaf)


class Identifier(Node):
    def __init__(self, leaf):
        super().__init__("Ident", children=None, leaf=leaf)


class Deref(Node):
    def __init__(self, leaf):
        super().__init__("Deref", children=None, leaf=leaf)

    def eval(self):
        lookup_rs = self.symbol_table.lookup(self.leaf)
        if lookup_rs:
            self.value = lookup_rs
        else:
            self.value = self.check_for_errs(
                self.children, f"muuttujaa {self.leaf} ei ole määritelty"
            )


class StringLiteral(Node):
    def __init__(self, leaf):
        super().__init__("StringLiteral", children=None, leaf=leaf)


class If(Node):
    def __init__(self, children, leaf):
        super().__init__("If", children, leaf)

    def eval(self):
        if self.leaf.value == TokenType.TRUE:
            print("tokentype true")
            self.value = self.children[0]
        elif self.leaf.value == TokenType.FALSE:
            print("tokentype false")
            self.value = None
        else:
            self.value = self.check_for_errs(self.children)
            print("If-noden lehden arvo ei ollut TRUE tai FALSE")


class IfElse(Node):
    def __init__(self, children, leaf):
        super().__init__("IfElse", children, leaf)
