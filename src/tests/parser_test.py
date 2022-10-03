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

    def test_parser_proc_decl(self):
        test_string = "to foo end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs), (StatementList)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_proc_decl_one_arg(self):
        test_string = "to foo :bar end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs, children: [:bar]), (StatementList)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_proc_decl_multiple_args(self):
        test_string = "to foo :bar :foobar end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs, children: [:bar, :foobar]), (StatementList)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_proc_decl_statement(self):
        test_string = "to foo show 123 end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs), (StatementList, children: [(TokenType.SHOW, children: [(Float, 123.0)])])])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_proc_decl_one_arg_and_statement(self):
        test_string = "to foo :x show :x end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs, children: [:x]), (StatementList, children: [(TokenType.SHOW, children: [(Deref, x)])])])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_proc_decl_multiple_args_and_statement(self):
        test_string = "to foo :x :y show :x end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs, children: [:x, :y]), (StatementList, children: [(TokenType.SHOW, children: [(Deref, x)])])])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_output_with_deref(self):
        test_string = "output :foo"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.OUTPUT, children: [(Deref, foo)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_output_with_float(self):
        test_string = "output 10"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.OUTPUT, children: [(Float, 10.0)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_output_with_string_literal(self):
        test_string = "output \"foo"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.OUTPUT, children: [(StringLiteral, foo)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_output_with_bool(self):
        test_string = "output true"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.OUTPUT, children: [(Bool, TokenType.TRUE)])])])"
        self.assertEqual(str(ast), expected)
