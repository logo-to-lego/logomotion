from entities.symbol import Variable, Function
from entities.type import Type
from entities.logotypes import LogoType


def initialize_logo_functions(symbol_tables):
    symbol_tables.functions.insert("repeat", _repeat())
    return symbol_tables

def _repeat():
    fname = 'repeat'
    repeat_n = Variable("n", Type(logotype=LogoType.FLOAT))
    nameless = Variable("block", Type(logotype=LogoType.NAMELESS_FUNCTION))
    procedure = Function(
        fname, params=[repeat_n, nameless], typeclass=Type(logotype=LogoType.VOID,functions=set(fname))
    )
    return procedure
