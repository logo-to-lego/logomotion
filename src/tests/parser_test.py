import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer
from parser.parser import Parser
from parser import ast

class TestParser(unittest.TestCase):
    """Test class for testing parser"""

    def setUp(self):
        self.console_mock = Mock()
        self.lexer = Lexer()
        self.lexer.build()
        self.parser = Parser(self.lexer)
        self.parser.build()

    def test_parser_start_node(self):
        test_string = 'show "ijsdijs'
        res = self.parser.parse(test_string)
        start_instance = ast.Start()
        self.assertEqual(type(res), type(start_instance))

    def test_parser_statementlist(self):
        test_string = 'show (23+32*19)'
        res = self.parser.parse(test_string)
        print(res.children[0])
        print(type(res.children[0]))
        st_instance = ast.StatementList()
        print(st_instance)
        print(type(st_instance))
        self.assertEqual(type(res.children[0]), type(st_instance))