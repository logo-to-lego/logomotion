"""Symbol table module"""

class SymbolTable:
    """A class for storing symbols and their values"""

    def __init__(self):
        """Initializes a new symbol table object"""
        self._table = {}
        self._stack = [self._table]

    def insert(self, symbol, value):
        """Inserts a new entry to the symbol table"""
        self._table[symbol] = value

    def lookup(self, symbol):
        """Searches for a symbol and returns it's value"""
        return self._table[symbol]

    def free(self):
        """Removes entries from a current symbol table"""
        self._table = {}

    def initialize_scope(self):
        """Saves current symbol table entries to a stack when entering to a new scope"""
        self._stack.append(self._table)
        copy = self._table.copy()
        self._table = copy

    def finalize_scope(self):
        """Restores previous symbol table entries from a previous scope and discards
           entries from a current scope"""
        if len(self._stack) > 1:
            self._stack.pop()
            self._table = self._stack[0]
            return True
        return False

default_symbol_table = SymbolTable()
