"""Symbol table module"""
from collections import deque

from entities.symbol import Variable


class SymbolTable:
    """A class for storing symbols and their values"""

    def __init__(self):
        """Initializes a new symbol table object"""
        self._stack = deque()
        self._stack.appendleft({})
        self._in_function = None

    def insert(self, key, value: Variable): # varsinaista arvoa ei tallenneta TODO Ota Variable pois 
        """Inserts a new entry to the symbol table"""
        self._stack[0][key] = value

    def lookup(self, key):
        """Searches for a symbol and returns its value.
        Global scope can't be reached in function scope"""
        if self._in_function:
            for i in range(len(self._stack) - 1):
                if key in self._stack[i]:
                    return self._stack[i][key]
        else:
            for table in self._stack:
                if key in table:
                    return table[key]
        return None

    def free(self):
        """Removes entries from the current symbol table scope"""
        self._stack[0] = {}

    def initialize_scope(self, in_function=None):
        """Saves current symbol table entries to a stack when entering to a new scope"""
        self._stack.appendleft({})
        self._in_function = in_function

    def finalize_scope(self):
        """Restores the previous symbol table scope and discards the current scope"""
        if len(self._stack) > 1:
            self._stack.popleft()
            if len(self._stack) == 1:
                self._in_function = None
            return True
        return False

    def insert_global(self, symbol, value):
        """Inserts a global scope entry to the symbol table"""
        self._stack[len(self._stack) - 1][symbol] = value

    def is_scope_global(self):
        """returns True if scope is global"""
        if len(self._stack) == 1:
            return True
        return False

    def get_current_scope(self):
        """return current scope as dict"""
        return self._stack[0]

    def get_in_scope_fuction_symbol(self):
        """Return the current in-scope function's symbol,
        or None when not currently in a function scope."""
        return self._in_function


default_variable_table = SymbolTable()
default_function_table = SymbolTable()
