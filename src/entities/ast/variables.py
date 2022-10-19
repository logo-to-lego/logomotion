from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Variable


class Float(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Float", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.FLOAT

        return self._logo_type

    def check_types(self):
        pass

    def generate_code(self):
        temp_var = self.generate_temp_var()
        code = f"double {temp_var} = {self.leaf};"
        self._logger.debug(code)
        self._code_generator.append_code(code)
        return temp_var


class Bool(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Bool", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.BOOL

        return self._logo_type

    def check_types(self):
        pass


class Deref(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Deref", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.UNKNOWN

        symbol = self._get_symbol()

        if symbol:
            self._logo_type = symbol.type

        return self._logo_type

    def set_type(self, new_type: LogoType):
        self._logo_type = new_type

        symbol = self._get_symbol()

        if symbol and symbol.type == LogoType.UNKNOWN:
            symbol.type = new_type

    def _get_symbol(self) -> Variable:
        return self._symbol_tables.variables.lookup(self.leaf)

    def check_types(self):
        symbol = self._get_symbol()
        if not symbol:
            self._logger.error_handler.add_error(2007, var=self.leaf)
        elif symbol.type != self.get_type():
            self._logger.error_handler.add_error(
                2008,
                var=self.leaf,
                curr_type=symbol.type.value,
                expected_type=self._logo_type.value,
            )


class StringLiteral(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("StringLiteral", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.STRING

        return self._logo_type

    def check_types(self):
        pass
