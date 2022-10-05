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
        """Searches for a symbol and returns its value.
        Global scope can't be reached from other scopes"""
        if len(self._stack) > 1:
            for i in range(0, len(self._stack)-1):
                if symbol in self._stack[i]:
                    return self._stack[i][symbol]
        else:
            if symbol in self._stack[0]:
                return self._stack[0][symbol]
        return None

    def free(self):
        """Removes entries from the current symbol table scope"""
        self._stack[0] = {}

    def initialize_scope(self):
        """Saves current symbol table entries to a stack when entering to a new scope"""
        self._stack.appendleft({})

    def finalize_scope(self):
        """Restores the previous symbol table scope and discards the current scope"""
        if len(self._stack) > 1:
            self._stack.popleft()
            return True
        return False

    def insert_global(self, symbol, value):
        """Inserts a global scope entry to the symbol table"""
        self._stack[len(self._stack)-1][symbol] = value

    def is_scope_global(self):
        """returns True if scope is global"""
        if len(self._stack) == 1:
            return True
        return False

    def get_current_scope(self):
        """return current scope as dict"""
        return self._stack[0]


default_symbol_table = SymbolTable()
