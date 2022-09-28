# pylint: disable=unused-argument,wildcard-import,unused-wildcard-import
""" Value product rules, for show and make commands """
from parser.globals import *
from parser import ast


def p_value_expression(prod):
    "value : expression"
    prod[0] = prod[1]


def p_value_deref(prod):
    "value : DEREF"
    prod[0] = ast.Deref((prod[1][1:]))
    prod[0].eval()


def p_value_string_literal(prod):
    "value : STRINGLITERAL"
    prod[0] = ast.StringLiteral(prod[1][1:])


def p_values(prod):
    "values : value values"
    prod[0] = [prod[1]] + prod[2]


def p_values_empty(prod):
    "values : empty"
    prod[0] = []
