# pylint: disable=unused-argument,wildcard-import,unused-wildcard-import,line-too-long
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
    | bye
    | if
    | ifelse"""
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
    "show : SHOW expression"
    prod[0] = ast.Command(lexer.reserved_words[prod[1]], [prod[2]])


def p_show_paren(prod):
    "show : LPAREN SHOW expression expressions RPAREN"
    prod[0] = ast.Command(lexer.reserved_words[prod[2]], [prod[3]] + prod[4])


def p_make(prod):
    """make : MAKE expression expression"""
    prod[0] = ast.Command(lexer.reserved_words[prod[1]], children=[prod[3]], leaf=prod[2])


def p_make_paren(prod):
    "make : LPAREN MAKE expression expression RPAREN"
    prod[0] = ast.Command(lexer.reserved_words[prod[2]], children=[prod[4]], leaf=prod[3])


def p_bye(prod):
    "bye : BYE"
    prod[0] = ast.Command(lexer.reserved_words[prod[1]])


def p_bye_paren(prod):
    "bye : LPAREN BYE RPAREN"
    prod[0] = ast.Command(lexer.reserved_words[prod[2]])


def p_if(prod):
    "if : IF LBRACE expression RBRACE LBRACE statement_list RBRACE"
    prod[0] = ast.If(children=[prod[6]], leaf=prod[3])


def p_if_paren(prod):
    "if : LPAREN IF LBRACE expression RBRACE LBRACE statement_list RBRACE RPAREN"
    prod[0] = ast.If(children=[prod[7]], leaf=prod[4])


def p_if_without_braces(prod):
    "if : IF expression LBRACE statement_list RBRACE"
    prod[0] = ast.If(children=[prod[4]], leaf=prod[2])


def p_if_without_braces_paren(prod):
    "if : LPAREN IF expression LBRACE statement_list RBRACE RPAREN"
    prod[0] = ast.If(children=[prod[5]], leaf=prod[3])


def p_ifelse(prod):
    "ifelse : IFELSE LBRACE expression RBRACE LBRACE statement_list RBRACE LBRACE statement_list RBRACE"
    prod[0] = ast.IfElse([prod[6], prod[9]], prod[3])


def p_ifelse_paren(prod):
    "ifelse : LPAREN IFELSE LBRACE expression RBRACE LBRACE statement_list RBRACE LBRACE statement_list RBRACE RPAREN"
    prod[0] = ast.IfElse([prod[7], prod[10]], prod[4])


def p_ifelse_without_braces(prod):
    "ifelse : IFELSE expression LBRACE statement_list RBRACE LBRACE statement_list RBRACE"
    prod[0] = ast.IfElse([prod[4], prod[7]], prod[2])


def p_ifelse_without_braces_paren(prod):
    "ifelse : LPAREN IFELSE expression LBRACE statement_list RBRACE LBRACE statement_list RBRACE RPAREN"
    prod[0] = ast.IfElse([prod[5], prod[8]], prod[3])
