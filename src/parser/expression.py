# pylint: disable=unused-argument,wildcard-import,unused-wildcard-import
"""Expression product rules"""
from parser.globals import *
from parser import ast


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
    prod[0] = ast.BinOp([prod[1], prod[3]], prod[2])


def p_expression_relop(prod):
    """expression : expression EQUALS expression
    | expression LESSTHAN expression
    | expression GREATERTHAN expression
    | expression LTEQUALS expression
    | expression GTEQUALS expression"""
    prod[0] = ast.RelOp([prod[1], prod[3]], prod[2])


def p_expression_uminus(prod):
    "expression : MINUS expression %prec UMINUS"
    prod[0] = ast.UnaryOp([prod[2]], "-")


def p_expression_group(prod):
    "expression : LPAREN expression RPAREN"
    prod[0] = prod[2]


def p_expression_number(prod):
    "expression : NUMBER"
    prod[0] = ast.Float(prod[1])


def p_expression_float(prod):
    "expression : FLOAT"
    prod[0] = ast.Float(prod[1])


def p_expression_bool(prod):
    """expression : TRUE
    | FALSE"""
    prod[0] = ast.Bool(shared.reserved_words[prod[1]])


def p_expression_deref(prod):
    "expression : DEREF"
    prod[0] = ast.Deref(prod[1][1:])


def p_expression_string_literal(prod):
    "expression : STRINGLITERAL"
    prod[0] = ast.StringLiteral(prod[1][1:])


def p_expression_proc_call(prod):
    "expression : proc_call"
    prod[0] = prod[1]
