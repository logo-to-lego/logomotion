"""Module for a class holding both function and variable symbol tables"""

from entities.symbol_table import default_variable_table, default_function_table
from entities.type import Type


class SymbolTables:
    "Utility class for symbol tables."

    def __init__(self, variables=default_variable_table, functions=default_function_table) -> None:
        self.variables = variables
        self.functions = functions

    def concatenate_typeclasses(self, symbol1, symbol2):
        """Takes two symbols (variable or function) as parameters,
        concatenates their typeclasses and updates their symbols typeclasses
        """

        typeclass1 = symbol1.typeclass
        typeclass2 = symbol2.typeclass
        new_typeclass = Type.concatenate(typeclass1, typeclass2)

        for variable in self.variables.get_symbols():
            if variable.typeclass in (typeclass1, typeclass2):
                variable.typeclass = new_typeclass

        for function in self.functions.get_symbols():
            if function.typeclass in (typeclass1, typeclass2):
                function.typeclass = new_typeclass

default_symbol_tables = SymbolTables()
