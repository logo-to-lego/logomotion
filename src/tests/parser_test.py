import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer
from parser.parser import Parser
from parser import ast


class TestParser(unittest.TestCase):
    """Test class for testing parser"""

    def setUp(self):
        self.console_mock = Mock()
        self.lexer = Lexer(console_io=self.console_mock)
        self.lexer.build()
        self.parser = Parser(self.lexer, console_io=self.console_mock)
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
        print(st_instance)
        print(type(st_instance))
        self.assertEqual(type(res.children[0]), type(st_instance))

    def test_parser_non_existing_proc_call_causes_syntax_error(self):
        test_string = "foo"
        ast = self.parser.parse(test_string)
        self.console_mock.write.assert_called()
        self.assertIn("Syntax", self.console_mock.write.call_args.args[0])

    def test_parser_make_call_is_parsed_correctly(self):
        test_string = 'make "var 10'
        ast = self.parser.parse(test_string)
        correct_result = "(Start, children: [(StatementList, children: [(TokenType.MAKE, var, children: [(Number, 10)])])])"
        self.assertEqual(str(ast), correct_result)

        test_string = 'make "var :10'
        ast = self.parser.parse(test_string)
        correct_result = "(Start, children: [(StatementList, children: [(TokenType.MAKE, var, children: [(Deref, 10)])])])"
        self.assertEqual(str(ast), correct_result)

        test_string = 'make "var "10'
        ast = self.parser.parse(test_string)
        correct_result = "(Start, children: [(StatementList, children: [(TokenType.MAKE, var, children: [(StringLiteral, 10)])])])"
        self.assertEqual(str(ast), correct_result)

    def test_parser_if_is_parsed_correctly(self):
        test_string = r"if true { show 10}"
        ast = self.parser.parse(test_string)
        correct_result = "(Start, children: [(StatementList, children: [(If, (Bool, TokenType.TRUE), children: [(StatementList, children: [(TokenType.SHOW, children: [(Number, 10)])])])])])"
        self.assertEqual(str(ast), correct_result)

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
