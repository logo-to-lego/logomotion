# pylint: disable=unused-argument,wildcard-import,unused-wildcard-import
"""Expression product rules"""
from parser.globals import *
from entities.ast.conditionals import *
from entities.ast.functions import *
from entities.ast.logocommands import *
from entities.ast.operations import *
from entities.ast.statementlist import *
from entities.ast.variables import *


def p_expressions(prod):
    "expressions : expressions expression"
    prod[0] = prod[1] + [prod[2]]


def p_expressions_empty(prod):
    "expressions : empty"
    prod[0] = []


def p_expression_binop(prod):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression MUL expression
    | expression DIV expression"""
    prod[0] = shared.node_factory.create_node(
        BinOp, children=[prod[1], prod[3]], leaf=prod[2], position=Position(prod)
    )


def p_expression_relop(prod):
    """expression : expression EQUALS expression
    | expression LESSTHAN expression
    | expression GREATERTHAN expression
    | expression LTEQUALS expression
    | expression GTEQUALS expression
    | expression NOTEQUALS expression"""
    prod[0] = shared.node_factory.create_node(
        RelOp, children=[prod[1], prod[3]], leaf=prod[2], position=Position(prod)
    )


def p_expression_uminus(prod):
    "expression : MINUS expression %prec UMINUS"
    prod[0] = shared.node_factory.create_node(
        UnaryOp, children=[prod[2]], leaf="-", position=Position(prod)
    )


def p_expression_group(prod):
    "expression : LPAREN expression RPAREN"
    prod[0] = prod[2]


def p_expression_number(prod):
    "expression : NUMBER"
    prod[0] = shared.node_factory.create_node(Float, leaf=prod[1], position=Position(prod))


def p_expression_float(prod):
    "expression : FLOAT"
    prod[0] = shared.node_factory.create_node(Float, leaf=prod[1], position=Position(prod))


def p_expression_bool(prod):
    """expression : TRUE
    | FALSE"""
    prod[0] = shared.node_factory.create_node(
        Bool, leaf=shared.reserved_words[prod[1]], position=Position(prod)
    )


def p_expression_deref(prod):
    "expression : DEREF"
    prod[0] = shared.node_factory.create_node(Deref, leaf=prod[1][1:], position=Position(prod))


def p_expression_string_literal(prod):
    "expression : STRINGLITERAL"
    prod[0] = shared.node_factory.create_node(
        StringLiteral, leaf=prod[1][1:], position=Position(prod)
    )


def p_expression_proc_call(prod):
    "expression : proc_call"
    prod[0] = prod[1]

def p_expression_block(prod):
    "expression : block"
    prod[0] = prod[1]