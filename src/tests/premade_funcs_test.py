"""Test module for preconfigured functions"""

import unittest
from entities.preconfigured_functions import initialize_logo_functions

class TestPremadeFuncs(unittest.TestCase):
    """
    """
    
    def setUp(self):
        console_io = Mock()
        self.error_handler = ErrorHandlerMock()
        self.logger = Logger(console_io=console_io, error_handler=self.error_handler)
        self.lexer = Lexer(self.logger)
        self.lexer.build()
        self.symbol_tables = SymbolTables(SymbolTable(), SymbolTable())
        self.parser = Parser(self.lexer, self.logger, self.symbol_tables)

