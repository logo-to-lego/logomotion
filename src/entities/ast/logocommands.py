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

        # Check first argument type and variable name
        var_name_node = self.leaf
        var_name = var_name_node.leaf
        var_name_type = var_name_node.get_type()

        if var_name_type == LogoType.UNKNOWN:
            var_name_node.set_type(LogoType.STRING)
        elif var_name_node.get_type() != LogoType.STRING:
            self._logger.error_handler.add_error(
                2010,
                row=self.position.get_pos()[0],
                command=self.type.value,
                curr_type=var_name_node.get_type().value,
                expected_type=LogoType.STRING.value,
            )
        var_name_node.check_types()

        # Check second argument type, assignment value
        value = self.children[0]
        logotype_of_value = value.get_type()
        print("LOGOTYPE OF VALUE", logotype_of_value)

        # Check if variable uses another variable as value, e.g. 'make "a :b'
        ref = self._symbol_tables.variables.lookup(value.leaf)
        symbol = self._symbol_tables.variables.lookup(var_name_node.leaf) # instance of Variable

        if ref and symbol:
            ref_type = ref.typeclass.logotype
            symbol_type = symbol.typeclass.logotype
            # pitäis kattoa unknownit
            if ref_type != symbol_type:
                self._logger.error_handler.add_error(
                    2012,
                    row=self.position.get_pos()[0],
                    var_name=var_name,
                    curr_type=symbol_type,
                    expected_type=ref_type,
                )
            else:
                # konkatenoi tyyppiluokat
                pass
        
        if ref and not symbol:
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
            print("END RESULT", symbol)
            print("\n••••")
            return

        # Check if var_name has symbol in symbol table
        if symbol and not ref:
            print("SYMBOL", symbol)
            print("VALUE", value)
            print()
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
        else:
            symbol = Variable(var_name, Type(
                logotype_of_value, variables={var_name}))
            self._symbol_tables.variables.insert(var_name, symbol)


        # Check if value is type of void
        if logotype_of_value == LogoType.VOID:
            self._logger.error_handler.add_error(
                2011,
                row=self.position.get_pos()[0],
                command=self.type.value,
                value_type=logotype_of_value.value,
            )
        value.check_types()

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
            self._logger.error_handler.add_error(
                2013, row=self.position.get_pos()[0])

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
        child_type = child.get_type()
        if child_type == LogoType.UNKNOWN:
            child.set_type(LogoType.FLOAT)
        elif child_type != LogoType.FLOAT:
            self._logger.error_handler.add_error(
                2010,
                row=child.position.get_pos()[0],
                command=self.type.value,
                curr_type=child_type.value,
                expected_type=LogoType.FLOAT.value,
            )
        child.check_types()

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
