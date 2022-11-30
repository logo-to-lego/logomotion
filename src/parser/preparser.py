"""Module for handling pre-parsing of the logo code. During pre-parsing we go through
the program code and find TO-function declarations and create grammar rule functions
from them. These are later added to the parser grammar, so that the user can call
procedures without parantheses."""

from parser.globals import Position
from lexer.lexer import Lexer
from lexer.token_types import TokenType
from entities.ast.functions import ProcCall
from entities.ast.node import NodeFactory
from utils.logger import default_logger


class Preparser:
    """Preparser is used to create new grammar rules from the program code, to allow
    the user to call procedures without parantheses."""

    def __init__(self, lexer: Lexer, node_factory: NodeFactory, logger=default_logger):
        self._lexer = lexer
        self._logger = logger
        self._node_factory = node_factory
        self._grammar_rules = {}

    def reset(self):
        self._grammar_rules = {}

    def export_grammar_rules(self, code):
        """Create and export procedure call grammar rules as a dict with the parse function
        name as key, and the parse function as value. Function names are added to the lexer
        tokens list."""

        tokens = self._lexer.tokenize_input(code)
        to_indices = [
            index for index, token in enumerate(tokens) if token.type == TokenType.TO.value
        ]

        for index in to_indices:
            self._create_procedure_rules(index, tokens)

        return self._grammar_rules

    def _create_procedure_rules(self, index, tokens):
        """Create the two rules for calling the procedure declared at index of the tokens list."""
        procedure_name = self._get_procedure_name(index + 1, tokens)
        procedure_param_count = self._get_procedure_param_count(index + 2, tokens)

        if not procedure_name or procedure_name in self._lexer.get_procedure_tokens():
            return

        procedure_count = len(self._grammar_rules)

        mangled_name = self._get_new_procedure_name(procedure_count)

        p_proc_call = self._create_call_rule(mangled_name, procedure_param_count)
        p_proc_call_paren = self._create_call_with_parantheses_rule(mangled_name)

        # Add the 2 rules to the rules dict.
        self._grammar_rules[f"p_preparser_proc{procedure_count}_call"] = p_proc_call
        self._grammar_rules[f"p_preparser_proc{procedure_count}_call_paren"] = p_proc_call_paren

        # Add token to Lexer tokens list.
        self._lexer.add_procedure_token(procedure_name, mangled_name)

        self._logger.debug(
            f"User defined procedure '{procedure_name}' found, internal token '{mangled_name}'"
        )

    def _get_new_procedure_name(self, procedure_count):
        """Returns a new procedure token name to be used by the lexer/parser."""
        mangled_name = f"PROC{procedure_count}"
        return mangled_name

    def _create_call_rule(self, procedure_name, procedure_param_count):
        "Create grammar rule for procedure call without parantheses. Returns a function."

        def p_proc_call(prod):
            prod[0] = self._node_factory.create_node(
                ProcCall,
                children=list(prod[2 : 2 + procedure_param_count]),
                leaf=prod[1],
                position=Position(prod),
            )

        # Define the grammar rule as a docstring.
        p_proc_call.__doc__ = f"proc_call : {procedure_name} "
        p_proc_call.__doc__ += " ".join(["expression"] * procedure_param_count)

        return p_proc_call

    def _create_call_with_parantheses_rule(self, procedure_name):
        "Create grammar rule for procedure call with paratheses. Returns a function."

        def p_proc_call_paren(prod):
            "proc_call : LPAREN IDENT expressions RPAREN"
            prod[0] = self._node_factory.create_node(
                ProcCall,
                children=prod[3],
                leaf=prod[2],
                position=Position(prod),
            )

        p_proc_call_paren.__doc__ = f"proc_call : LPAREN {procedure_name} expressions RPAREN"

        return p_proc_call_paren

    def _get_procedure_name(self, index, tokens):
        """Get the procedure name (not token) located at index."""
        if index >= len(tokens):
            return None

        name_token = tokens[index]

        if name_token.type != TokenType.IDENT.value:
            return None

        return name_token.value.lower()

    def _get_procedure_param_count(self, index, tokens):
        """Get the procedure param count with the param tokens starting at the given index."""
        if index >= len(tokens):
            return 0

        param_count = 0

        for token in tokens[index:]:
            if token.type != TokenType.DEREF.value:
                break
            param_count += 1

        return param_count
