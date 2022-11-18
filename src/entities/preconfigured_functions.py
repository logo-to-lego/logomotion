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
    symbol_tables.functions.insert("for", _for())
    return symbol_tables


def _repeat():
    """Definition for repeat/toista nameless function
    Returns
        class Function
    """
    # fname is the name that will be called from functions table
    fname = "repeat"
    # initialize params as variables
    repeat_n = Variable("n", Type(logotype=LogoType.FLOAT))
    nameless = Variable("block", Type(logotype=LogoType.NAMELESS_FUNCTION))
    # Initialize function, pass name and parans, define typeclass
    # typeclasses logotype should reflect the return value
    procedure = Function(
        fname,
        params=[repeat_n, nameless],
        typeclass=Type(logotype=LogoType.VOID, functions=set((fname,))),
    )
    return procedure

#Typical for loop. The controllist specifies three or four members: 
# the local varname, start value, limit value, and optional step size
def _for():
    """Definition for 'for' nameless function
    Returns
    
    """
    fname = "for"
    iterator_name = Variable("iterator_name", Type(logotype=LogoType.STRING))
    start = Variable("start", Type(logotype=LogoType.FLOAT))
    limit = Variable("limit", Type(logotype=LogoType.FLOAT))
    stepsize = Variable("stepsize", Type(logotype=LogoType.FLOAT))
    nameless = Variable("block", Type(logotype=LogoType.NAMELESS_FUNCTION))
    procedure = Function(
        fname,
        params=[iterator_name, start, limit, stepsize, nameless],
        typeclass=Type(logotype=LogoType.VOID, functions=set((fname,))),
    )
    return procedure
    
    