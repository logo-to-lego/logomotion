"""Module for a class holding both function and variable symbol tables"""

from entities.symbol_table import default_variable_table, default_function_table


class SymbolTables:
    "Utility class for symbol tables."

    def __init__(self, variables=default_variable_table, functions=default_function_table) -> None:
        self.variables = variables
        self.functions = functions


default_symbol_tables = SymbolTables()
