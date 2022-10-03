# pylint: disable=unused-argument,wildcard-import,unused-wildcard-import

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
from parser.expression import *
from ply import yacc
from lexer.lexer import Lexer


def p_start(prod):
    "start : statement_list"
    prod[0] = ast.Start([prod[1]])


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
    lineno = lexer.ply.lineno
    colpos = lexer.ply.lexpos - lexer.ply.linestartpos

    if prod:
        console.write(f"Syntax error at '{prod.value}' ({lineno}, {colpos})")
    else:
        console.write(f"Syntax error at {lineno}, {colpos}")


class Parser:
    """Wrapper class for parser functionality. Used to transform source code into AST."""

    def __init__(self, current_lexer: Lexer, console_io=None) -> None:
        self._current_lexer = current_lexer
        lexer.update(current_lexer)
        globals()["tokens"] = current_lexer.tokens
        self._parser = None

        if console_io:
            globals()["console"] = console_io

    def build(self, **kwargs):
        """Builds the PLY parser. Passes arguments to PLY's yacc.yacc()."""
        self._parser = yacc.yacc(**kwargs)

    def parse(self, code, **kwargs):
        """Calls the PLY parser on given code and parser arguments.

        Args:
            code (str): Logo source code.

        Returns:
            start_node (parser.ast.Start): AST
        """
        self._current_lexer.reset()
        ply_parser = self.get_ply_parser()
        ply_lexer = self._current_lexer.get_ply_lexer()

        start_node = ply_parser.parse(code, lexer=ply_lexer, **kwargs)

        return start_node

    def get_ply_parser(self, **kwargs):
        """Returns the built PLY parser. Automatically calls build() if it doesn't exist."""
        if not self._parser:
            self.build(**kwargs)
        return self._parser
