"""Symbol table module"""
from collections import deque


class SymbolTable:
    """A class for storing symbols and their values"""

    def __init__(self):
        """Initializes a new symbol table object"""
        self._stack = deque()
        self._stack.appendleft({})

    def insert(self, symbol, value):
        """Inserts a new entry to the symbol table"""
        self._stack[0][symbol] = value

    def lookup(self, symbol):
        """Searches for a symbol and returns it's value"""
        for table in self._stack:
            if symbol in table:
                return table[symbol]
        return None

    def free(self):
        """Removes entries from a current symbol table"""
        self._stack[0] = {}

    def initialize_scope(self):
        """Saves current symbol table entries to a stack when entering to a new scope"""
        self._stack.appendleft({})

    def finalize_scope(self):
        """Restores previous symbol table entries from a previous scope and discards
        entries from a current scope"""
        if len(self._stack) > 1:
            self._stack.popleft()
            return True
        return False


default_symbol_table = SymbolTable()
