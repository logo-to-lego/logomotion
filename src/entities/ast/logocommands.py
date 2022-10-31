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

    def check_types(self):
        print("\nMAKE CHECK TYPES", self.leaf.leaf, "\n")
        # Check for right amount of params
        if len(self.children) != 1 or not self.leaf:
            self._logger.error_handler.add_error(
                2009, row=self.position.get_pos()[0], command=self.type.value
            )
            return

        # Check that variable name is string
        var_name_node = self.leaf
        var_name_node.check_types()
        var_name = var_name_node.leaf
        if var_name_node.get_type() != LogoType.STRING:
            self._logger.error_handler.add_error(
                2010,
                row=self.position.get_pos()[0],
                command=self.type.value,
                curr_type=var_name_node.get_type().value,
                expected_type=LogoType.STRING.value,
            )

        # Check second argument type, assignment value
        value = self.children[0]
        value.check_types()
        logotype_of_value = value.get_type()

        # Check if value is type of void
        if logotype_of_value == LogoType.VOID:
            self._logger.error_handler.add_error(
                2011,
                row=self.position.get_pos()[0],
                command=self.type.value,
                value_type=logotype_of_value.value,
            )

        # Symbol reference e.g. make "a :b, where ref is :b
        ref = self._symbol_tables.variables.lookup(value.leaf)

        # Check if the symbol has already been defined. E.g. make "a 2, where :a has been defined before this make statement
        symbol = self._symbol_tables.variables.lookup(var_name_node.leaf)

        # e.g. make "a 3, where :a has not been defined before
        if (not ref) and (not symbol):
            print("1, 2")
            symbol = Variable(var_name, Type(logotype_of_value, variables={var_name}))
            self._symbol_tables.variables.insert(var_name, symbol)

        # e.g. make "b :a, where :b has not been defined before, but :a has been defined
        elif ref and not symbol:
            print("5")
            if logotype_of_value in (LogoType.UNKNOWN, ref.typeclass.logotype):
                ref.typeclass.add_variable(var_name)
                symbol = Variable(var_name, ref.typeclass)
                self._symbol_tables.variables.insert(var_name, symbol)
            else:
                self._logger.error_handler.add_error(
                    2012,
                    row=self.position.get_pos()[0],
                    var_name=var_name,
                    curr_type=logotype_of_value,
                    expected_type=ref.typeclass.logotype,
                )

        # e.g. make "b 42, where :b has been defined before
        elif not ref and symbol:
            print("3")
            if symbol.typeclass.logotype == LogoType.UNKNOWN:
                symbol.typeclass.logotype = logotype_of_value
            elif logotype_of_value == LogoType.UNKNOWN:
                value.set_type(symbol.typeclass.logotype)
            elif value.get_type() != symbol.typeclass.logotype:
                self._logger.error_handler.add_error(
                    2012,
                    row=self.position.get_pos()[0],
                    var_name=var_name,
                    curr_type=symbol.typeclass.logotype.value,
                    expected_type=value.get_type().value,
                )
        
        else: # ref and symbol
            print("4")
            # e.g. make "b :a, where :b and :a have been defined earlier
            ref_type = ref.typeclass.logotype
            symbol_type = symbol.typeclass.logotype

            if (ref_type == LogoType.UNKNOWN) or (symbol_type == LogoType.UNKNOWN) or (ref_type == symbol_type):
                # concatenate typeclasses
                self._symbol_tables.variables.concatenate_typeclasses(ref, symbol)
            else:
                self._logger.error_handler.add_error(
                    2012,
                    row=self.position.get_pos()[0],
                    var_name=var_name,
                    curr_type=symbol_type,
                    expected_type=ref_type,
                )



        print("END RESULT", symbol)
        print("\n••••")
        


class Show(Node):
    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.VOID
        return self._logo_type

    def check_types(self):
        # Must have at least 1 param
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
