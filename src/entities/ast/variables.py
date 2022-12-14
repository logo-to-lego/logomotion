from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Variable
from entities.type import Type
from utils.lowercase_converter import convert_to_lowercase as to_lowercase


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
            self._logger.error_handler.add_error(
                "undefined_variable", self.position.get_lexspan(), var=self.leaf
            )
        else:
            # We need to set the symbol ref here,
            # since the symbol table is not fully accessible after type checking.
            self.set_symbol(symbol)

    def generate_code(self):
        return self._code_generator.variable_name(to_lowercase(self.leaf))


class StringLiteral(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("StringLiteral", children=None, leaf=leaf, **dependencies)

    def get_logotype(self):
        return LogoType.STRING

    def generate_code(self):
        return self._code_generator.string(self.leaf)


class VariableNode(Node):
    """Used as the first argument in for argument list"""

    def __init__(self, leaf, **dependencies):
        super().__init__("VariableNode", children=None, leaf=leaf, **dependencies)

    def get_logotype(self):
        return LogoType.STRING

    def check_types(self):
        """Type check is passed as scoped_type_check
        will be called from unknown_function node"""
        # pylint: disable=W0107
        pass

    def scoped_type_check(self):
        symbol = Variable(self.leaf, Type(LogoType.FLOAT, variables={self.leaf}))
        self._symbol_tables.variables.insert(self.leaf.leaf, symbol)

    def generate_code(self):
        tmpvar = self._code_generator.float(0)
        self._code_generator.create_new_variable(to_lowercase(self.leaf.leaf), tmpvar)
        return tmpvar
