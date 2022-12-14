from entities.symbol import Variable, Function
from entities.type import Type
from entities.logotypes import LogoType


def initialize_logo_functions(function_tables):
    """Initializes premade functions to symbol table, such as repeat/toista
    Args
        symbol_tables: class SymbolTables
    Returns
        symbol_tables: class SymbolTables
    """
    function_tables.insert("for", _for())
    function_tables.insert("repeat", _repeat())
    return function_tables

def _repeat():
    """Definition for repeat/toista nameless function
    Returns
        class Function
    """
    # fname is the name that will be called from functions table
    fname = "repeat"
    # initialize params as variables
    repeat_n = Variable("n", Type(logotype=LogoType.FLOAT))
    nameless = Variable("nameless", Type(logotype=LogoType.NAMELESS_FUNCTION))
    # Initialize function, pass name and parans, define typeclass
    # typeclasses logotype should reflect the return value
    procedure = Function(
        fname,
        params=[repeat_n, nameless],
        typeclass=Type(logotype=LogoType.VOID),
    )
    return procedure

def _for():
    """Definition for 'for' nameless function
    Returns
        class Function
    """
    fname = "for"
    iterator_name = Variable("iterator_name", Type(logotype=LogoType.STRING))
    start = Variable("start", Type(logotype=LogoType.FLOAT))
    limit = Variable("limit", Type(logotype=LogoType.FLOAT))
    stepsize = Variable("stepsize", Type(logotype=LogoType.FLOAT))
    nameless = Variable("nameless", Type(logotype=LogoType.NAMELESS_FUNCTION))
    procedure = Function(
        fname,
        params=[iterator_name, start, limit, stepsize, nameless],
        typeclass=Type(logotype=LogoType.VOID),
    )
    return procedure
