# pylint: disable=unused-argument,wildcard-import,unused-wildcard-import
""" Command production rules
"""
from parser.globals import *
from parser import ast


def p_command(prod):
    """command : fd
    | bk
    | lt
    | rt
    | show
    | make
    | bye"""
    prod[0] = prod[1]


def p_fd(prod):
    "fd : FD expression"
    prod[0] = ast.Command(lexer.reserved_words[prod[1]], [prod[2]])


def p_fd_paren(prod):
    "fd : LPAREN FD expression RPAREN"
    prod[0] = ast.Command(lexer.reserved_words[prod[2]], [prod[3]])


def p_bk(prod):
    "bk : BK expression"
    prod[0] = ast.Command(lexer.reserved_words[prod[1]], [prod[2]])


def p_bk_paren(prod):
    "bk : LPAREN BK expression RPAREN"
    prod[0] = ast.Command(lexer.reserved_words[prod[2]], [prod[3]])


def p_lt(prod):
    "lt : LT expression"
    prod[0] = ast.Command(lexer.reserved_words[prod[1]], [prod[2]])


def p_lt_paren(prod):
    "lt : LPAREN LT expression RPAREN"
    prod[0] = ast.Command(lexer.reserved_words[prod[2]], [prod[3]])


def p_rt(prod):
    "rt : RT expression"
    prod[0] = ast.Command(lexer.reserved_words[prod[1]], [prod[2]])


def p_rt_paren(prod):
    "rt : LPAREN RT expression RPAREN"
    prod[0] = ast.Command(lexer.reserved_words[prod[2]], [prod[3]])


def p_show(prod):
    "show : SHOW value"
    prod[0] = ast.Command(lexer.reserved_words[prod[1]], [prod[2]])


def p_show_paren(prod):
    "show : LPAREN SHOW value values RPAREN"
    prod[0] = ast.Command(lexer.reserved_words[prod[2]], [prod[3]] + prod[4])


def p_make(prod):
    """make : MAKE STRINGLITERAL value"""
    prod[0] = ast.Command(lexer.reserved_words[prod[1]], children=[prod[3]], leaf=prod[2][1:])


def p_bye(prod):
    "bye : BYE"
    prod[0] = ast.Command(lexer.reserved_words[prod[1]])
