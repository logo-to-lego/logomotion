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
        test_string = "show (23+32*19)"
        res = self.parser.parse(test_string)
        st_instance = ast.StatementList()
        self.assertEqual(type(res.children[0]), type(st_instance))

    """
    def test_parser_fd(self):
        test_string = "fd 5"
        exp_str = "(Start, children: [(StatementList, children: [(TokenType.FD, children: [(Number, 5)])])])"
        res = self.parser.parse(test_string)
        res_str = res.__str__()
        self.assertEqual(res_str, exp_str)

    def test_parser_div_paren(self):
        test_string = "show (5+2)/2"
        exp_str = "(Start, children: [(StatementList, children: [(TokenType.SHOW, children: [(BinOp, /, children: [(BinOp, +, children: [(Number, 5), (Number, 2)]), (Number, 2)])])])])"
        res = self.parser.parse(test_string)
        res_str = res.__str__()
        self.assertEqual(res_str, exp_str)
    """
