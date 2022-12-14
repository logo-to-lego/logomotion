"""Test module for preconfigured functions"""
from lexer.lexer import Lexer
from parser.parser import Parser
from utils.error_handler_mock import ErrorHandlerMock
from code_generator.code_generator import default_code_generator
from utils.logger import Logger
from entities.preconfigured_functions import initialize_logo_functions
from entities.symbol_table import SymbolTable
from entities.symbol_tables import SymbolTables
from unittest.mock import Mock
import unittest

class TestPremadeFuncs(unittest.TestCase):
    """
    """
    
    def setUp(self):
        console_io = Mock()
        self.error_handler = ErrorHandlerMock()
        self.logger = Logger(console_io=console_io, error_handler=self.error_handler)
        self.lexer = Lexer(self.logger)
        self.lexer.build()
        fs = initialize_logo_functions(SymbolTable())
        self.symbol_tables = SymbolTables(SymbolTable(), functions=fs)
        self.parser = Parser(self.lexer, self.logger, self.symbol_tables)

    def tearDown(self):
        default_code_generator.reset()
    
    def test_double_repeat(self):
        test_code = "REPEAT 2 {fd 20}\
            REPEAT 3 {fd 40}"
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(0,len(self.error_handler.get_error_ids()))
        
    def test_for_in_for(self):
        test_code = """
        for ["i 1 2 1] { ;itr start limit step
            for ["j 1 3 1] {
            show :j
            }
        }"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(0,len(self.error_handler.get_error_ids()))
        
    def test_repeat_in_for(self):
        test_code = """for ["i 0 3 1] {
            repeat :i {
                show :i+10
            }
        }"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        self.assertEqual(0,len(self.error_handler.get_error_ids()))
    
    def test_for_not_enough_args(self):
        test_code = """for ["a 1 2] {fd 20}"""
        ast = self.parser.parse(test_code)
        ast.check_types()
        error_ids = self.error_handler.get_error_ids()
        self.assertIn("wrong_amount_of_aguments_for_procedure" , error_ids)