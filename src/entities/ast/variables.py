from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Variable
from entities.type import Type


class Float(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Float", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.FLOAT

        return self._logo_type

    def check_types(self):
        self.get_type()

    def generate_code(self):
        return self._code_generator.float(self.leaf)


class Bool(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Bool", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.BOOL

        return self._logo_type

    def check_types(self):
        self.get_type()


class Deref(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Deref", children=None, leaf=leaf, **dependencies)

    def get_type(self) -> LogoType:
        symbol = self._get_symbol()
        if symbol:
            return symbol.typeclass.logotype
        return None

    def get_typeclass(self) -> Type:
        symbol = self._get_symbol()
        if symbol:
            return symbol.typeclass
        return None

    def _get_symbol(self) -> Variable:
        symbol = self._symbol_tables.variables.lookup(self.leaf)
        if symbol:
            return symbol
        return None

    def check_types(self):
        symbol = self._get_symbol()
        if not symbol:
            self._logger.error_handler.add_error(2007, var=self.leaf)

class StringLiteral(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("StringLiteral", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.STRING

        return self._logo_type

    def check_types(self):
        self.get_type()
