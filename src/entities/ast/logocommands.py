from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Variable
from lexer.token_types import TokenType


class Make(Node):
    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.VOID
        return self._logo_type

    def check_types(self):
        # Check for right amount of params
        if len(self.children) != 1 or not self.leaf:
            self._logger.error_handler.add_error(
                2009, row=self.position.get_pos()[0], command=self.type.value
            )
            return

        # Check first argument type and variable name
        var_name = self.leaf
        var_name_type = var_name.get_type()

        if var_name_type == LogoType.UNKNOWN:
            var_name.set_type(LogoType.STRING)
        elif var_name.get_type() != LogoType.STRING:
            self._logger.error_handler.add_error(
                2010,
                row=self.position.get_pos()[0],
                command=self.type.value,
                curr_type=var_name.get_type().value,
                expected_type=LogoType.STRING.value,
            )
        var_name.check_types()

        # Check second argument type, assignment value
        value = self.children[0]
        value_type = value.get_type()

        if value_type == LogoType.VOID:
            self._logger.error_handler.add_error(
                2011,
                row=self.position.get_pos()[0],
                command=self.type.value,
                value_type=value_type.value,
            )
        value.check_types()

        # Check if var_name has symbol in symbol table
        symbol = self._symbol_tables.variables.lookup(var_name.leaf)
        if symbol:
            if symbol.type == LogoType.UNKNOWN:
                symbol.type = value.get_type()
            elif value.get_type() == LogoType.UNKNOWN:
                value.set_type(symbol.type)
            elif value.get_type() != symbol.type:
                self._logger.error_handler.add_error(
                    2012,
                    row=self.position.get_pos()[0],
                    var_name=var_name.leaf,
                    curr_type=symbol.type.value,
                    expected_type=value.get_type().value,
                )
        else:
            symbol = Variable(var_name.leaf, value.get_type())
            self._symbol_tables.variables.insert(var_name.leaf, symbol)


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
