from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Variable
from entities.type import Type
from lexer.token_types import TokenType
from utils.lowercase_converter import convert_to_lowercase as to_lowercase


class Make(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("Make", children, leaf, **dependencies)
        self._new_variable = False

    def get_logotype(self):
        return LogoType.VOID

    def _check_variable_node(self, variable_node):
        # Check that variable name is string
        if variable_node.node_type == "Deref":
            self._logger.error_handler.add_error(
                "deref_instead_of_string_literal",
                lexspan=self.position.get_lexspan(),
                var_name=variable_node.leaf
            )
            return

        variable_node.check_types()
        variable_logotype = variable_node.get_logotype()

        if variable_logotype != LogoType.STRING:
            self._logger.error_handler.add_error(
                "wrong_param_type",
                lexspan=self.position.get_lexspan(),
                row=self.position.get_pos()[0],
                command=self.node_type,
                curr_type=variable_node.get_logotype().value,
                expected_type=LogoType.STRING.value,
            )

    def _check_argument_node(self, argument_node):
        # Check type of argument
        argument_node.check_types()
        arg_logotype = argument_node.get_logotype()

        if arg_logotype == LogoType.VOID:
            self._logger.error_handler.add_error(
                "type_cannot_be_assigned_to_a_variable",
                self.position.get_lexspan(),
                curr_type=arg_logotype
            )

    def _create_new_variable(self, name, logotype):
        symbol = Variable(name, Type(logotype, variables={name}))
        self._symbol_tables.variables.insert(name, symbol)

    def _create_new_variable_with_referenced_value(self, name, arg_logotype, typeclass):
        if arg_logotype in (LogoType.UNKNOWN, typeclass.logotype):
            typeclass.add_variable(name)
            symbol = Variable(name, typeclass)
            self._symbol_tables.variables.insert(name, symbol)
        else:
            self._logger.error_handler.add_error(
                "variable_type_cannot_be_changed",
                self.position.get_lexspan(),
                row=self.position.get_pos()[0],
                var_name=name,
                curr_type=arg_logotype,
                expected_type=typeclass.logotype,
            )

    def _update_variable_type(self, name, var_symbol: Variable, arg_node):
        var_type = var_symbol.typeclass.logotype
        arg_type = arg_node.get_logotype()

        if var_type == LogoType.UNKNOWN:
            var_symbol.typeclass.logotype = arg_type
        elif var_type != arg_type:
            self._logger.error_handler.add_error(
                "variable_type_cannot_be_changed",
                self.position.get_lexspan(),
                row=self.position.get_pos()[0],
                var_name=name,
                curr_type=var_type.value,
                expected_type=arg_type.value,
            )

    def _update_variable_type_with_referenced_value(self, name, reference_node, symbol_node):
        ref_type = reference_node.typeclass.logotype
        symbol_type = symbol_node.typeclass.logotype
        if (
            (ref_type == LogoType.UNKNOWN)
            or (symbol_type == LogoType.UNKNOWN)
            or (ref_type == symbol_type)
        ):
            self._symbol_tables.concatenate_typeclasses(reference_node, symbol_node)
        else:
            self._logger.error_handler.add_error(
                "variable_type_cannot_be_changed",
                self.position.get_lexspan(),
                row=self.position.get_pos()[0],
                var_name=name,
                curr_type=symbol_type,
                expected_type=ref_type,
            )

    def _check_references(self, var_node, arg_node):
        # Check if the symbol has already been defined
        var_name = var_node.leaf
        var_symbol = self._symbol_tables.variables.lookup(var_name)
        # Check if referenced value has already been defined.
        # e.g. 'make "b :a', where the referenced value is 'a'
        arg_symbol = None
        if arg_node.node_type == "Deref":
            arg_name = arg_node.leaf
            arg_symbol = self._symbol_tables.variables.lookup(arg_name)
        elif arg_node.node_type == "ProcCall":
            arg_name = arg_node.leaf
            arg_symbol = self._symbol_tables.functions.lookup(arg_name)

        arg_logotype = arg_node.get_logotype()

        if not var_symbol:
            self._new_variable = True

        if not var_symbol and not arg_symbol:
            # e.g. 'make "a 2', where 'a' has not been defined before
            self._create_new_variable(var_name, arg_logotype)

        elif not var_symbol and arg_symbol:
            # e.g. 'make "b :a', where 'b' has not been defined before, but 'a' has been defined
            self._create_new_variable_with_referenced_value(
                var_name, arg_logotype, arg_symbol.typeclass
            )

        elif var_symbol and not arg_symbol:
            # e.g. 'make "b 42', where 'b' has already been defined
            self._update_variable_type(var_name, var_symbol, arg_node)

        else:  # var_symbol and arg_symbol
            # e.g. 'make "b :a', where 'a' and 'b' have been defined earlier
            self._update_variable_type_with_referenced_value(var_name, arg_symbol, var_symbol)

    def check_types(self):
        # Check for right amount of arguments
        if len(self.children) != 1 or not self.leaf:
            self._logger.error_handler.add_error(
                "wrong_amount_of_arguments",
                self.position.get_lexspan(),
                row=self.position.get_pos()[0],
                command=self.node_type.value,
            )
            return

        variable_node = self.leaf
        argument_node = self.children[0]

        self._check_variable_node(variable_node)
        self._check_argument_node(argument_node)
        self._check_references(variable_node, argument_node)

    def generate_code(self):
        """Generates MAKE command into target code."""
        value_var_name = self.children[0].generate_code()

        if self._new_variable:
            self._code_generator.create_new_variable(to_lowercase(self.leaf.leaf), value_var_name)
        else:
            self._code_generator.assign_value(to_lowercase(self.leaf.leaf), value_var_name)


class Show(Node):
    def get_logotype(self):
        return LogoType.VOID

    def check_types(self):
        # Must have at least 1 argument
        if len(self.children) == 0:
            self._logger.error_handler.add_error(
                "wrong_amount_of_arguments",
                self.position.get_lexspan())

        # Cannot be function call that returns VOID
        for child in self.children:
            logo_type = child.get_logotype()
            if logo_type == LogoType.VOID:
                self._logger.error_handler.add_error(
                    "wrong_param_type",
                    self.position.get_lexspan(),
                    command=self.node_type.value,
                    curr_type=LogoType.VOID.value,
                )
            child.check_types()

    def generate_code(self):
        for child in self.children:
            arg_var = child.generate_code()
            self._code_generator.show(arg_var)


class Bye(Node):
    def get_logotype(self):
        return LogoType.VOID

    def check_types(self):
        return

    def generate_code(self):
        self._code_generator.bye()


class Move(Node):
    """FD, BK, LT, RT"""

    def get_logotype(self):
        return LogoType.VOID

    def check_types(self):
        if len(self.children) != 1:
            self._logger.error_handler.add_error(
                "wrong_amount_of_arguments",
                self.position.get_lexspan(),
                row=self.position.get_pos()[0],
                command=self.node_type.value,
            )
            return

        child = self.children[0]
        child.check_types()

        if child.node_type == "Deref" and child.get_logotype() == LogoType.UNKNOWN:
            child.set_logotype(LogoType.FLOAT)

        if child.get_logotype() is None:
            return

        if child.get_logotype() != LogoType.FLOAT:
            self._logger.error_handler.add_error(
                "wrong_param_type",
                self.position.get_lexspan(),
                row=child.position.get_pos()[0],
                command=self.node_type.value,
                curr_type=child.get_logotype().value,
                expected_type=LogoType.FLOAT.value,
            )

    def generate_code(self):
        """Generate movement commands in Java."""
        arg_var = self.children[0].generate_code()

        if self.node_type == TokenType.FD:
            self._code_generator.move_forward(arg_var)
        if self.node_type == TokenType.BK:
            self._code_generator.move_backwards(arg_var)
        if self.node_type == TokenType.LT:
            self._code_generator.left_turn(arg_var)
        if self.node_type == TokenType.RT:
            self._code_generator.right_turn(arg_var)
