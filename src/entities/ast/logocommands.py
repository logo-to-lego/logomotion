from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Variable
from entities.type import Type
from lexer.token_types import TokenType


class Make(Node):
    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.VOID
        return self._logo_type

    def _check_variable_node(self, variable_node):
        # Check that variable name is string
        variable_node.check_types()
        variable_logotype = variable_node.get_type()

        if variable_logotype != LogoType.STRING:
            self._logger.error_handler.add_error(
                2010,
                row=self.position.get_pos()[0],
                command=self.type.value,
                curr_type=variable_node.get_type().value,
                expected_type=LogoType.STRING.value,
            )

    def _check_argument_node(self, argument_node):
        # Check type of argument
        argument_node.check_types()
        arg_logotype = argument_node.get_type()

        if arg_logotype == LogoType.VOID:
            self._logger.error_handler.add_error(
                2011,
                row=self.position.get_pos()[0],
                command=self.type.value,
                value_type=arg_logotype.value,
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
                2012,
                row=self.position.get_pos()[0],
                var_name=name,
                curr_type=arg_logotype,
                expected_type=typeclass.logotype,
            )

    def _update_variable_type(self, name, arg_node, symbol_logotype, arg_logotype):
        if symbol_logotype == LogoType.UNKNOWN:
            symbol_logotype = arg_logotype
        elif arg_logotype == LogoType.UNKNOWN:
            arg_node.set_type(symbol_logotype)
        elif arg_node.get_type() != symbol_logotype:
            self._logger.error_handler.add_error(
                2012,
                row=self.position.get_pos()[0],
                var_name=name,
                curr_type=symbol_logotype.value,
                expected_type=arg_node.get_type().value,
            )

    def _update_variable_type_with_referenced_value(self, name, reference_node, symbol_node):
        ref_type = reference_node.typeclass.logotype
        symbol_type = symbol_node.typeclass.logotype
        if (
            (ref_type == LogoType.UNKNOWN)
            or (symbol_type == LogoType.UNKNOWN)
            or (ref_type == symbol_type)
        ):
            self._symbol_tables.variables.concatenate_typeclasses(reference_node, symbol_node)
        else:
            self._logger.error_handler.add_error(
                2012,
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
        if arg_node.type == "Deref":
            arg_name = arg_node.leaf
            arg_symbol = self._symbol_tables.variables.lookup(arg_name)
            arg_node.set_symbol(arg_symbol)

        arg_logotype = arg_node.get_type()

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
            self._update_variable_type(
                var_name, arg_node, var_symbol.typeclass.logotype, arg_logotype
            )

        else:  # var_symbol and arg_symbol
            # e.g. 'make "b :a', where 'a' and 'b' have been defined earlier
            self._update_variable_type_with_referenced_value(var_name, arg_symbol, var_symbol)

    def check_types(self):
        # Check for right amount of arguments
        if len(self.children) != 1 or not self.leaf:
            self._logger.error_handler.add_error(
                2009, row=self.position.get_pos()[0], command=self.type.value
            )
            return

        variable_node = self.leaf
        argument_node = self.children[0]

        self._check_variable_node(variable_node)
        self._check_argument_node(argument_node)
        self._check_references(variable_node, argument_node)


class Show(Node):
    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.VOID
        return self._logo_type

    def check_types(self):
        # Must have at least 1 argument
        if len(self.children) == 0:
            self._logger.error_handler.add_error(2013, row=self.position.get_pos()[0])

        # Cannot be function call that returns VOID
        for child in self.children:
            logo_type = child.get_type()
            if logo_type == LogoType.VOID:
                self._logger.error_handler.add_error(
                    2014,
                    row=child.position.get_pos()[0],
                    command=self.type.value,
                    return_type=LogoType.VOID.value,
                )
            child.check_types()


class Bye(Node):
    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.VOID
        return self._logo_type

    def check_types(self):
        if self.children:
            self._logger.error_handler.add_error(2015, command=self.type.value)


class Move(Node):
    """FD, BK, LT, RT"""

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.VOID
        return self._logo_type

    def check_types(self):
        if len(self.children) != 1:
            self._logger.error_handler.add_error(
                2009, row=self.position.get_pos()[0], command=self.type.value
            )
            return

        child = self.children[0]
        child.check_types()
        child_type = child.get_type()

        if child_type is None:
            return

        if child_type != LogoType.FLOAT:
            self._logger.error_handler.add_error(
                2010,
                row=child.position.get_pos()[0],
                command=self.type.value,
                curr_type=child_type.value,
                expected_type=LogoType.FLOAT.value,
            )

    def generate_code(self):
        """Generate movement commands in Java."""
        arg_var = self.children[0].generate_code()

        if self.type == TokenType.FD:
            self._code_generator.move_forward(arg_var)
        if self.type == TokenType.BK:
            self._code_generator.move_backwards(arg_var)
        if self.type == TokenType.LT:
            self._code_generator.left_turn(arg_var)
        if self.type == TokenType.RT:
            self._code_generator.right_turn(arg_var)
