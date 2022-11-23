from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Variable
from entities.type import Type


class Float(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Float", children=None, leaf=leaf, **dependencies)

    def get_logotype(self):
        return LogoType.FLOAT

    def generate_code(self):
        return self._code_generator.float(self.leaf)


class Bool(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Bool", children=None, leaf=leaf, **dependencies)

    def get_logotype(self):
        return LogoType.BOOL

    def generate_code(self):
        return self._code_generator.boolean(self.leaf)


class Deref(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Deref", children=None, leaf=leaf, **dependencies)
        self._symbol: Variable = None

    def set_symbol(self, symbol: Variable):
        if symbol != self.get_symbol():
            raise Exception(
                (
                    f"Bug: variable symbol param {symbol} and the symbol defined"
                    f"in symbol_table {self.get_symbol()} do not match"
                )
            )
        self._symbol = symbol

    def set_logotype(self, logotype):
        symbol = self.get_symbol()
        if symbol:
            symbol.typeclass.logotype = logotype

    def get_logotype(self) -> LogoType:
        symbol = self.get_symbol()
        if symbol:
            return symbol.typeclass.logotype
        return None

    def get_typeclass(self) -> Type:
        symbol = self.get_symbol()
        if symbol:
            return symbol.typeclass
        return None

    def get_symbol(self) -> Variable:
        if self._symbol:
            return self._symbol
        return self._symbol_tables.variables.lookup(self.leaf)

    def check_types(self):
        symbol = self.get_symbol()
        if not symbol:
            self._logger.error_handler.add_error(2007, var=self.leaf)

    def generate_code(self):
        return self._code_generator.variable_name(self.leaf.lower())


class StringLiteral(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("StringLiteral", children=None, leaf=leaf, **dependencies)

    def get_logotype(self):
        return LogoType.STRING

    def generate_code(self):
        return self._code_generator.string(self.leaf)
