"""Module for handling pre-parsing of the logo code. During pre-parsing we go through the program code
and find TO-function declarations and create grammar rule functions from them. These are later added
to the parser grammar, so that the user can call procedures without parantheses."""

from lexer.lexer import Lexer
from lexer.token_types import TokenType
from entities.ast.functions import ProcCall
from parser.globals import Position, shared
from utils.logger import default_logger


class Preparser:
    """Preparser is used to create new grammar rules from the program code, to allow the user to call
    procedures without parantheses."""

    def __init__(self, lexer: Lexer, logger=default_logger):
        self._lexer = lexer
        self._logger = logger
        self._grammar_rules = dict()

    def export_grammar_rules(self, code):
        """Create and export procedure call grammar rules as a dict with the parse function name as key,
        and the parse function as value."""

        tokens = self._lexer.tokenize_input(code)
        to_indices = [index for index, token in enumerate(tokens) if token == TokenType.TO]

        for index in to_indices:
            self._create_procedure_rules(index, tokens)

        return self._grammar_rules

    def _create_procedure_rules(self, index, tokens):
        """Create the two rules for calling the procedure declared at index of the tokens list."""
        procedure_name = self._get_procedure_name(index + 1, tokens)
        procedure_param_count = self._get_procedure_param_count(index + 2, tokens)

        if not procedure_name:
            return

        # The proc_call function definition
        def p_proc_call(prod):
            prod[0] = shared.node_factory.create_node(
                ProcCall,
                children=[product for product in prod[3:3 + procedure_param_count]],
                leaf=prod[2],
                position=Position(prod),
            )

        # Create the grammar rule (doc string).
        p_proc_call.__doc__ = f"proc_call : {procedure_name} "
        p_proc_call.__doc__ += " ".join(["expression"] * procedure_param_count)

        procedure_count = len(self._grammar_rules)

        # Add the 2 rules to the rules dict.
        self._grammar_rules[f"p_proc{procedure_count}_call"] = p_proc_call

    def _get_procedure_name(self, index, tokens):
        """Get the procedure name (not token) located at index."""
        if index >= len(tokens):
            return None

        name_token = tokens[index]

        if name_token != TokenType.IDENT:
            return None

        return name_token.value

    def _get_procedure_param_count(self, index, tokens):
        """Get the procedure param count with the param tokens starting at the given index."""
        if index >= len(tokens):
            return 0

        param_count = 0

        for token in tokens[index:]:
            if token != TokenType.DEREF:
                break
            param_count += 1

        return param_count
