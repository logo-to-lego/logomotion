# pylint: disable=unused-argument,wildcard-import,unused-wildcard-import,line-too-long
""" Command production rules
"""
from parser.globals import *
from entities.ast.conditionals import *
from entities.ast.functions import *
from entities.ast.logocommands import *
from entities.ast.operations import *
from entities.ast.statementlist import *
from entities.ast.variables import *
from entities.ast.unknown_function import *
from lexer.token_types import TokenType


def p_statement(prod):
    """statement : fd
    | bk
    | lt
    | rt
    | show
    | make
    | bye
    | if
    | ifelse
    | proc_decl
    | output
    | proc_call"""
    prod[0] = prod[1]


def p_fd(prod):
    "fd : FD expression"
    prod[0] = shared.node_factory.create_node(
        Move,
        node_type=shared.reserved_words[prod[1]],
        children=[prod[2]],
        position=Position(prod),
    )


def p_fd_paren(prod):
    "fd : LPAREN FD expression RPAREN"
    prod[0] = shared.node_factory.create_node(
        Move,
        node_type=shared.reserved_words[prod[2]],
        children=[prod[3]],
        position=Position(prod),
    )


def p_bk(prod):
    "bk : BK expression"
    prod[0] = shared.node_factory.create_node(
        Move,
        node_type=shared.reserved_words[prod[1]],
        children=[prod[2]],
        position=Position(prod),
    )


def p_bk_paren(prod):
    "bk : LPAREN BK expression RPAREN"
    prod[0] = shared.node_factory.create_node(
        Move,
        node_type=shared.reserved_words[prod[2]],
        children=[prod[3]],
        position=Position(prod),
    )


def p_lt(prod):
    "lt : LT expression"
    prod[0] = shared.node_factory.create_node(
        Move,
        node_type=shared.reserved_words[prod[1]],
        children=[prod[2]],
        position=Position(prod),
    )


def p_lt_paren(prod):
    "lt : LPAREN LT expression RPAREN"
    prod[0] = shared.node_factory.create_node(
        Move,
        node_type=shared.reserved_words[prod[2]],
        children=[prod[3]],
        position=Position(prod),
    )


def p_rt(prod):
    "rt : RT expression"
    prod[0] = shared.node_factory.create_node(
        Move,
        node_type=shared.reserved_words[prod[1]],
        children=[prod[2]],
        position=Position(prod),
    )


def p_rt_paren(prod):
    "rt : LPAREN RT expression RPAREN"
    prod[0] = shared.node_factory.create_node(
        Move,
        node_type=shared.reserved_words[prod[2]],
        children=[prod[3]],
        position=Position(prod),
    )


def p_show(prod):
    "show : SHOW expression"
    prod[0] = shared.node_factory.create_node(
        Show,
        node_type=shared.reserved_words[prod[1]],
        children=[prod[2]],
        position=Position(prod),
    )


def p_show_paren(prod):
    "show : LPAREN SHOW expression expressions RPAREN"
    prod[0] = shared.node_factory.create_node(
        Show,
        node_type=shared.reserved_words[prod[2]],
        children=[prod[3]] + prod[4],
        position=Position(prod),
    )


def p_make(prod):
    """make : MAKE expression expression"""
    prod[0] = shared.node_factory.create_node(
        Make,
        children=[prod[3]],
        leaf=prod[2],
        position=Position(prod),
    )


def p_make_paren(prod):
    "make : LPAREN MAKE expression expression RPAREN"
    prod[0] = shared.node_factory.create_node(
        Make,
        children=[prod[4]],
        leaf=prod[3],
        position=Position(prod),
    )


def p_proc_decl(prod):
    "proc_decl : TO IDENT proc_args statement_list END"
    prod[0] = shared.node_factory.create_node(
        ProcDecl, children=[prod[3], prod[4]], leaf=prod[2], position=Position(prod)
    )


def p_proc_args(prod):
    "proc_args : proc_args DEREF"
    argument = shared.node_factory.create_node(ProcArg, leaf=prod[2][1:], position=Position(prod))
    prod[0] = shared.node_factory.create_node(
        ProcArgs, children=prod[1].children + [argument], position=Position(prod)
    )


def p_output(prod):
    "output : OUTPUT expression"
    prod[0] = shared.node_factory.create_node(
        Output,
        node_type=shared.reserved_words[prod[1]],
        children=[prod[2]],
        position=Position(prod),
    )


def p_proc_args_empty(prod):
    "proc_args : empty"
    prod[0] = shared.node_factory.create_node(ProcArgs, children=[], position=Position(prod))


def p_proc_call(prod):
    "proc_call : LPAREN IDENT expressions RPAREN"
    prod[0] = shared.node_factory.create_node(
        ProcCall,
        children=prod[3],
        leaf=prod[2],
        position=Position(prod),
    )

def p_for_call(prod): #for ["i 1 2 3] {}
    "proc_call : FOR LBRACKET expressions RBRACKET unknown_function"
    #unknown_f = shared.node_factory.create_node(
    #    UnknownFunction,
    #    arg_type = LogoType.FLOAT,
    #    children=[prod[6]],
    #    position=Position(prod),
    #    iter_param=prod[3][0]
    #)
    vnode = shared.node_factory.create_node(
            VariableNode,
            leaf=prod[3][0],
            position=Position(prod)
            )
    unf = prod[5]
    unf.var_node = vnode
    prod[0] = shared.node_factory.create_node(
        ProcCall,
        children=[vnode] + prod[3][1:] + [unf],
        leaf="for",
        position=Position(prod)
    )

def p_repeat_call(prod):
    "proc_call : REPEAT expression unknown_function"
    #"proc_call : REPEAT expressions LBRACE statement_list RBRACE"
    #unknown_f = shared.node_factory.create_node(
    #    UnknownFunction,
    #    arg_type = LogoType.VOID,
    #    children=[prod[4]],
    #    position=Position(prod)
    #)
    unf = prod[3]
    unf.arg_type = LogoType.VOID
    prod[0] = shared.node_factory.create_node(
        ProcCall,
        children=[prod[2]] + [unf],
        leaf = "repeat",
        position=Position(prod)
    )

def p_bye(prod):
    "bye : BYE"
    prod[0] = shared.node_factory.create_node(
        Bye, node_type=shared.reserved_words[prod[1]], position=Position(prod)
    )


def p_bye_paren(prod):
    "bye : LPAREN BYE RPAREN"
    prod[0] = shared.node_factory.create_node(
        Bye, node_type=shared.reserved_words[prod[2]], position=Position(prod)
    )


def p_if(prod):
    "if : IF LBRACE expression RBRACE unknown_function"
    prod[0] = shared.node_factory.create_node(
        If, children=prod[5].children, leaf=prod[3], position=Position(prod)
    )


def p_if_paren(prod):
    "if : LPAREN IF LBRACE expression RBRACE unknown_function RPAREN"
    prod[0] = shared.node_factory.create_node(
        If, children=prod[6].children, leaf=prod[4], position=Position(prod)
    )


def p_if_without_braces(prod):
    "if : IF expression unknown_function"
    prod[0] = shared.node_factory.create_node(
        If, children=prod[3].children, leaf=prod[2], position=Position(prod)
    )


def p_if_without_braces_paren(prod):
    "if : LPAREN IF expression unknown_function RPAREN"
    prod[0] = shared.node_factory.create_node(
        If, children=prod[4].children, leaf=prod[3], position=Position(prod)
    )


def p_ifelse(prod):
    "ifelse : IFELSE LBRACE expression RBRACE unknown_function unknown_function"
    prod[0] = shared.node_factory.create_node(
        IfElse,
        children=[prod[5].children[0], prod[6].children[0]],
        leaf=prod[3],
        position=Position(prod),
    )


def p_ifelse_paren(prod):
    "ifelse : LPAREN IFELSE LBRACE expression RBRACE unknown_function unknown_function RPAREN"
    prod[0] = shared.node_factory.create_node(
        IfElse,
        children=[prod[6].children[0], prod[7].children[0]],
        leaf=prod[4],
        position=Position(prod),
    )


def p_ifelse_without_braces(prod):
    "ifelse : IFELSE expression unknown_function unknown_function"
    prod[0] = shared.node_factory.create_node(
        IfElse,
        children=[prod[3].children[0], prod[4].children[0]],
        leaf=prod[2],
        position=Position(prod),
    )


def p_ifelse_without_braces_paren(prod):
    "ifelse : LPAREN IFELSE expression unknown_function unknown_function RPAREN"
    prod[0] = shared.node_factory.create_node(
        IfElse,
        children=[prod[4].children[0], prod[5].children[0]],
        leaf=prod[3],
        position=Position(prod),
    )
