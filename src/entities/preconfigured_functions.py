from entities.symbol import Variable, Function
from entities.type import Type
from entities.logotypes import LogoType


def initialize_logo_functions(symbol_tables):
    """Initializes premade functions to symbol table, such as repeat/toista
    Args
        symbol_tables: class SymbolTables
    Returns
        symbol_tables: class SymbolTables
    """
    symbol_tables.functions.insert("repeat", _repeat())
    return symbol_tables


def _repeat():
    """Definition for repeat/toista nameless function
    Returns
        class Function
    """
    fname = "repeat"
    repeat_n = Variable("n", Type(logotype=LogoType.FLOAT))
    nameless = Variable("block", Type(logotype=LogoType.NAMELESS_FUNCTION))
    procedure = Function(
        fname,
        params=[repeat_n, nameless],
        typeclass=Type(logotype=LogoType.VOID, functions=set((fname,))),
    )
    return procedure
