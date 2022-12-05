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
    | REPEAT

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

unknown_function
    : LBRACE statement_list RBRACE

list
    : LBRACKET statement_list RBRACKET

"""


from parser.globals import *
from parser.command import *
from parser.expression import *
from parser.preparser import Preparser
from ply import yacc
from lexer.lexer import Lexer
from utils.code_generator import default_code_generator
from utils.logger import default_logger
from entities.symbol_tables import default_symbol_tables

from entities.ast.node import *
from entities.ast.conditionals import *
from entities.ast.functions import *
from entities.ast.logocommands import *
from entities.ast.operations import *
from entities.ast.statementlist import *
from entities.ast.variables import *
from entities.ast.unknown_function import *


def p_start(prod):
    "start : statement_list"
    prod[0] = shared.node_factory.create_node(Start, children=[prod[1]], position=Position(prod))


def p_statement_list(prod):
    "statement_list : statement statement_list"
    prod[0] = shared.node_factory.create_node(
        StatementList, children=[prod[1]] + prod[2].children, position=Position(prod)
    )


def p_statement_list_empty(prod):
    "statement_list : empty"
    prod[0] = shared.node_factory.create_node(StatementList, position=Position(prod))


def p_unknown_function_statement_list(prod):
    "unknown_function : LBRACE statement_list RBRACE"
    prod[0] = shared.node_factory.create_node(\
        UnknownFunction, children=[prod[2]], position=Position(prod))


def p_empty(prod):
    "empty :"


# pylint: disable-next=missing-function-docstring
def p_error(prod):
    lineno = shared.ply_lexer.lineno
    colpos = shared.ply_lexer.lexpos - shared.ply_lexer.linestartpos
    if prod:
        lexspan = (prod.lexpos, prod.lexpos + len(prod.value) - 1)
        shared.logger.error_handler.add_error(
            2000, lexspan, row=lineno, column=colpos, prodval=prod.value
        )
    else:
        lexspan = (-1, -1)
        # täytyy sopia mitkä lexspan-arvot halutaan, kun ohjelma päättyy parser-virheeseen
        shared.logger.error_handler.add_error(2001, lexspan, row=lineno, column=colpos)


class Parser:
    """Wrapper class for parser functionality. Used to transform source code into AST."""

    def __init__(
        self,
        current_lexer: Lexer,
        logger=default_logger,
        symbol_tables=default_symbol_tables,
        code_generator=default_code_generator,
    ):
        self._current_lexer = current_lexer
        shared.update(current_lexer, logger, symbol_tables, code_generator)
        self._preparser = Preparser(current_lexer, shared.node_factory, logger)
        globals()["tokens"] = current_lexer.get_tokens()
        self._parser = None
        self._logger = logger

    def reset(self):
        "Resets the parser internals."

        # Initialize grammar to only contain non-preparser rules.
        preparser_rules = []

        for item in globals():
            if "p_preparser_" in item:
                preparser_rules.append(item)

        for rule in preparser_rules:
            globals().pop(rule)

        globals()["tokens"] = self._current_lexer.get_tokens()

    def _build(self, code, **kwargs):
        """Preparses the logo program for function declarations and builds the PLY parser.
        Clears previously added rules. Passes arguments to PLY's yacc.yacc()."""

        self.reset()
        self._current_lexer.reset()
        self._preparser.reset()

        for function_name, function in self._preparser.export_grammar_rules(code).items():
            self._logger.debug(f"Preparser procedure call grammar rule added: {function_name}")
            globals()[function_name] = function

        self._parser = yacc.yacc(**kwargs)

    def parse(self, code, **kwargs):
        """Builds the PLY parser and runs it on given code and parser arguments.

        Args:
            code (str): Logo source code.

        Returns:
            start_node (parser.ast.Start): AST
        """

        # Build the PLY parser with the added function tokens.
        self._build(code, **kwargs)

        ply_parser = self.get_ply_parser()
        ply_lexer = self._current_lexer.get_ply_lexer()

        start_node = ply_parser.parse(code, lexer=ply_lexer, tracking=True, **kwargs)

        return start_node

    def get_ply_parser(self, **kwargs):
        """Returns the built PLY parser."""
        return self._parser
