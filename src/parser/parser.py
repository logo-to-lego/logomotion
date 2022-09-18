# pylint: disable=unused-argument,wildcard-import,unused-wildcard-import, wrong-import-position

"""
Parser module using PLY. Create a new Parser object to use the parser.

Grammar, not all productions have been implemented/listed:

start
    : statement_list

statement_list
    : statement statement_list
    | empty

statement
    : command
    | procedure_decl

command
    : fd
    | bk
    | rt
    | lt
    | cs
    | show
    | make
    | procedure_call_no_params TODO
    | procedure_call_params TODO
    | IFE TODO
    | STOP TODO
    | FORE TODO
    | RUN TODO
    | REPEAT TODO

expression_list
    : expression expression_list
    | empty

procedure_call_no_params
    : IDENT

procedure_call_params
    : IDENT expression
    | LPAREN IDENT expression_list RPAREN

procedure_decl
    : TO IDENT param_decl_list statement_list END

param_decl_list
    : DEREF
    | DEREF COMMA param_decl_list

block
    : LBRACE statement_list RBRACE

list
    : LBRACKET statement_list RBRACKET

"""


from parser import ast
from parser.globals import *
from parser.command import *
from parser.value import *
from parser.expression import *
from ply import yacc
from lexer.lexer import Lexer


def p_start(prod):
    "start : statement_list"
    prod[0] = prod[1]


def p_statement_list(prod):
    "statement_list : statement statement_list"
    prod[0] = ast.StatementList([prod[1]] + prod[2].children)


def p_statement_list_empty(prod):
    "statement_list : empty"
    prod[0] = ast.StatementList()


def p_statement_command(prod):
    "statement : command"
    prod[0] = prod[1]


def p_empty(prod):
    "empty :"


# pylint: disable-next=missing-function-docstring
def p_error(prod):
    print(f"Syntax error at '{prod.value}'")


class Parser:
    """Wrapper class for parser functionality."""

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        globals()["tokens"] = lexer.tokens
        reserved_words.update(lexer.reserved_words)
        self.parser = None

    def build(self, **kwargs):
        """Builds the PLY parser. Passes arguments to yacc.yacc()."""
        self.parser = yacc.yacc(**kwargs)

    def parse(self, code, **kwargs):
        """Calls the PLY parser on given code and parser arguments.

        Args:
            code (str): Logo source code.

        Returns:
            node (parser.ast.Node): AST
        """
        parser = self.get_parser()
        return parser.parse(code, lexer=self.lexer.get_lexer(), **kwargs)

    def get_parser(self):
        """Returns PLY parser. Automatically calls build() if it doesn't exist."""
        if not self.parser:
            self.build()
        return self.parser
