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

        new_typeclass = Type.concatenate(symbol1.typeclass, symbol2.typeclass)

        for var_name in new_typeclass.variables:
            variable = self.variables.lookup(var_name)
            variable.typeclass = new_typeclass

        for func_name in new_typeclass.functions:
            func = self.functions.lookup(func_name)
            func.typeclass = new_typeclass


default_symbol_tables = SymbolTables()
