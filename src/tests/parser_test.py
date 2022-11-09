import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer
from parser.parser import Parser

from entities.ast.node import *
from entities.ast.conditionals import *
from entities.ast.functions import *
from entities.ast.logocommands import *
from entities.ast.operations import *
from entities.ast.statementlist import *
from entities.ast.variables import *

from utils.logger import Logger


class TestParser(unittest.TestCase):
    """Test class for testing parser"""

    def setUp(self):
        self.console_mock = Mock()
        self.error_mock = Mock()
        self.logger = Logger(self.console_mock, self.error_mock)
        self.lexer = Lexer(self.logger)
        self.lexer.build()
        self.parser = Parser(self.lexer, self.logger)
        self.parser.build()
        self.maxDiff = None

    def test_parser_start_node(self):
        test_string = 'show "ijsdijs'
        res = self.parser.parse(test_string)
        start_instance = Start()
        self.assertEqual(type(res), type(start_instance))

    def test_parser_statementlist(self):
        test_string = "show (23+32*19)"
        res = self.parser.parse(test_string)
        st_instance = StatementList()
        print(st_instance)
        print(type(st_instance))
        self.assertEqual(type(res.children[0]), type(st_instance))

    def test_parser_proc_decl(self):
        test_string = "to foo end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs), (StatementList)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_proc_decl_one_arg(self):
        test_string = "to foo :bar end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs, children: [(ProgArg, bar)]), (StatementList)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_proc_decl_multiple_args(self):
        test_string = "to foo :bar :foobar end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs, children: [(ProgArg, bar), (ProgArg, foobar)]), (StatementList)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_proc_decl_statement(self):
        test_string = "to foo show 123 end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs), (StatementList, children: [(TokenType.SHOW, children: [(Float, 123.0, logo type: LogoType.FLOAT)])])])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_proc_decl_one_arg_and_statement(self):
        test_string = "to foo :x show :x end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs, children: [(ProgArg, x)]), (StatementList, children: [(TokenType.SHOW, children: [(Deref, x)])])])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_proc_decl_multiple_args_and_statement(self):
        test_string = "to foo :x :y show :x end"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(ProcDecl, foo, children: [(ProcArgs, children: [(ProgArg, x), (ProgArg, y)]), (StatementList, children: [(TokenType.SHOW, children: [(Deref, x)])])])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_output_with_deref(self):
        test_string = "output :foo"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.OUTPUT, children: [(Deref, foo)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_output_with_float(self):
        test_string = "output 10"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.OUTPUT, children: [(Float, 10.0, logo type: LogoType.FLOAT)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_output_with_string_literal(self):
        test_string = 'output "foo'
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.OUTPUT, children: [(StringLiteral, foo, logo type: LogoType.STRING)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_output_with_bool(self):
        test_string = "output true"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.OUTPUT, children: [(Bool, TokenType.TRUE, logo type: LogoType.BOOL)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_make_call_is_parsed_correctly(self):
        test_string = 'make "var 10'
        ast = self.parser.parse(test_string)
        correct_result = "(Start, children: [(StatementList, children: [(TokenType.MAKE, (StringLiteral, var, logo type: LogoType.STRING), children: [(Float, 10.0, logo type: LogoType.FLOAT)])])])"
        self.assertEqual(str(ast), correct_result)

        test_string = 'make "var :10'
        ast = self.parser.parse(test_string)
        correct_result = "(Start, children: [(StatementList, children: [(TokenType.MAKE, (StringLiteral, var, logo type: LogoType.STRING), children: [(Deref, 10)])])])"
        self.assertEqual(str(ast), correct_result)

        test_string = 'make "var "10'
        ast = self.parser.parse(test_string)
        correct_result = "(Start, children: [(StatementList, children: [(TokenType.MAKE, (StringLiteral, var, logo type: LogoType.STRING), children: [(StringLiteral, 10, logo type: LogoType.STRING)])])])"
        self.assertEqual(str(ast), correct_result)

    def test_make_with_parenthesis(self):
        test_string = '(make "robot.move 1+2)'
        ast = self.parser.parse(test_string)
        correct_result = "(Start, children: [(StatementList, children: [(TokenType.MAKE, (StringLiteral, robot.move, logo type: LogoType.STRING), children: [(BinOp, +, logo type: LogoType.FLOAT, children: [(Float, 1.0, logo type: LogoType.FLOAT), (Float, 2.0, logo type: LogoType.FLOAT)])])])])"
        self.assertEqual(str(ast), correct_result)

    def test_parser_if_statementlist_brackets(self):
        test_string = r"if true { show 10}"
        ast = self.parser.parse(test_string)
        correct_result = "(Start, children: [(StatementList, children: [(If, (Bool, TokenType.TRUE, logo type: LogoType.BOOL), children: [(StatementList, children: [(TokenType.SHOW, children: [(Float, 10.0, logo type: LogoType.FLOAT)])])])])])"
        self.assertEqual(str(ast), correct_result)

    def test_parser_if_expression_and_statementlist_brackets(self):
        test_string = r"if {true} { show 10}"
        ast = self.parser.parse(test_string)
        correct_result = "(Start, children: [(StatementList, children: [(If, (Bool, TokenType.TRUE, logo type: LogoType.BOOL), children: [(StatementList, children: [(TokenType.SHOW, children: [(Float, 10.0, logo type: LogoType.FLOAT)])])])])])"
        self.assertEqual(str(ast), correct_result)

    def test_parser_if_statementlist_brackets_paren(self):
        test_string = r"(if true { show 10})"
        ast = self.parser.parse(test_string)
        correct_result = "(Start, children: [(StatementList, children: [(If, (Bool, TokenType.TRUE, logo type: LogoType.BOOL), children: [(StatementList, children: [(TokenType.SHOW, children: [(Float, 10.0, logo type: LogoType.FLOAT)])])])])])"
        self.assertEqual(str(ast), correct_result)

    def test_parser_fd(self):
        test_string = "fd 5"
        exp_str = "(Start, children: [(StatementList, children: [(TokenType.FD, children: [(Float, 5.0, logo type: LogoType.FLOAT)])])])"
        res = self.parser.parse(test_string)
        self.assertEqual(str(res), exp_str)

    def test_parser_fd_paren(self):
        test_string = "(fd 5)"
        exp_str = "(Start, children: [(StatementList, children: [(TokenType.FD, children: [(Float, 5.0, logo type: LogoType.FLOAT)])])])"
        res = self.parser.parse(test_string)
        self.assertEqual(str(res), exp_str)

    def test_parser_bk(self):
        test_string = "bk 1"
        exp_str = "(Start, children: [(StatementList, children: [(TokenType.BK, children: [(Float, 1.0, logo type: LogoType.FLOAT)])])])"
        res = self.parser.parse(test_string)
        self.assertEqual(str(res), exp_str)

    def test_parser_bk_paren(self):
        test_string = "(bk 1)"
        exp_str = "(Start, children: [(StatementList, children: [(TokenType.BK, children: [(Float, 1.0, logo type: LogoType.FLOAT)])])])"
        res = self.parser.parse(test_string)
        self.assertEqual(str(res), exp_str)

    def test_parser_rt(self):
        test_string = "rt 2.1"
        exp_str = "(Start, children: [(StatementList, children: [(TokenType.RT, children: [(Float, 2.1, logo type: LogoType.FLOAT)])])])"
        res = self.parser.parse(test_string)
        self.assertEqual(str(res), exp_str)

    def test_parser_rt_paren(self):
        test_string = "(rt 2.1)"
        exp_str = "(Start, children: [(StatementList, children: [(TokenType.RT, children: [(Float, 2.1, logo type: LogoType.FLOAT)])])])"
        res = self.parser.parse(test_string)
        self.assertEqual(str(res), exp_str)

    def test_parser_lt(self):
        test_string = "lt 4"
        exp_str = "(Start, children: [(StatementList, children: [(TokenType.LT, children: [(Float, 4.0, logo type: LogoType.FLOAT)])])])"
        res = self.parser.parse(test_string)
        self.assertEqual(str(res), exp_str)

    def test_parser_lt_paren(self):
        test_string = "(lt 4)"
        exp_str = "(Start, children: [(StatementList, children: [(TokenType.LT, children: [(Float, 4.0, logo type: LogoType.FLOAT)])])])"
        res = self.parser.parse(test_string)
        self.assertEqual(str(res), exp_str)

    def test_parser_show(self):
        test_string = 'show "a'
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.SHOW, children: [(StringLiteral, a, logo type: LogoType.STRING)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_show_paren_one_arg(self):
        test_string = '(show "a)'
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.SHOW, children: [(StringLiteral, a, logo type: LogoType.STRING)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_show_paren_multiple_arg(self):
        test_string = '(show "a "b "c)'
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.SHOW, children: [(StringLiteral, a, logo type: LogoType.STRING), (StringLiteral, b, logo type: LogoType.STRING), (StringLiteral, c, logo type: LogoType.STRING)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_show_with_single_quote(self):
        test_string = "(show 'a 'b 'c)"
        ast = self.parser.parse(test_string)
        expected = "(Start, children: [(StatementList, children: [(TokenType.SHOW, children: [(StringLiteral, a, logo type: LogoType.STRING), (StringLiteral, b, logo type: LogoType.STRING), (StringLiteral, c, logo type: LogoType.STRING)])])])"
        self.assertEqual(str(ast), expected)

    def test_parser_div_paren(self):
        test_string = "show (5+2)/2"
        exp_str = "(Start, children: [(StatementList, children: [(TokenType.SHOW, children: [(BinOp, /, logo type: LogoType.FLOAT, children: [(BinOp, +, logo type: LogoType.FLOAT, children: [(Float, 5.0, logo type: LogoType.FLOAT), (Float, 2.0, logo type: LogoType.FLOAT)]), (Float, 2.0, logo type: LogoType.FLOAT)])])])])"
        res = self.parser.parse(test_string)
        self.assertEqual(str(res), exp_str)

    def test_if(self):
        test_string = "if 1+1 < 3 { show 1 }"
        expected = "(Start, children: [(StatementList, children: [(If, (RelOp, <, logo type: LogoType.BOOL, children: [(BinOp, +, logo type: LogoType.FLOAT, children: [(Float, 1.0, logo type: LogoType.FLOAT), (Float, 1.0, logo type: LogoType.FLOAT)]), (Float, 3.0, logo type: LogoType.FLOAT)]), children: [(StatementList, children: [(TokenType.SHOW, children: [(Float, 1.0, logo type: LogoType.FLOAT)])])])])])"
        ast = self.parser.parse(test_string)
        self.assertEqual(str(ast), expected)

    def test_ifelse(self):
        test_string = "ifelse 1+1 < 3 { show 1 } { show 2}"
        expected = "(Start, children: [(StatementList, children: [(IfElse, (RelOp, <, logo type: LogoType.BOOL, children: [(BinOp, +, logo type: LogoType.FLOAT, children: [(Float, 1.0, logo type: LogoType.FLOAT), (Float, 1.0, logo type: LogoType.FLOAT)]), (Float, 3.0, logo type: LogoType.FLOAT)]), children: [(StatementList, children: [(TokenType.SHOW, children: [(Float, 1.0, logo type: LogoType.FLOAT)])]), (StatementList, children: [(TokenType.SHOW, children: [(Float, 2.0, logo type: LogoType.FLOAT)])])])])])"
        ast = self.parser.parse(test_string)
        self.assertEqual(str(ast), expected)

    def test_ifelse_paren(self):
        test_string = "(ifelse 1+1 < 3 { show 1 } { show 2})"
        expected = "(Start, children: [(StatementList, children: [(IfElse, (RelOp, <, logo type: LogoType.BOOL, children: [(BinOp, +, logo type: LogoType.FLOAT, children: [(Float, 1.0, logo type: LogoType.FLOAT), (Float, 1.0, logo type: LogoType.FLOAT)]), (Float, 3.0, logo type: LogoType.FLOAT)]), children: [(StatementList, children: [(TokenType.SHOW, children: [(Float, 1.0, logo type: LogoType.FLOAT)])]), (StatementList, children: [(TokenType.SHOW, children: [(Float, 2.0, logo type: LogoType.FLOAT)])])])])])"
        ast = self.parser.parse(test_string)
        self.assertEqual(str(ast), expected)

    def test_ifelse_paren_braces(self):
        test_string = "(ifelse {1+1 < 3} { show 1 } { show 2})"
        expected = "(Start, children: [(StatementList, children: [(IfElse, (RelOp, <, logo type: LogoType.BOOL, children: [(BinOp, +, logo type: LogoType.FLOAT, children: [(Float, 1.0, logo type: LogoType.FLOAT), (Float, 1.0, logo type: LogoType.FLOAT)]), (Float, 3.0, logo type: LogoType.FLOAT)]), children: [(StatementList, children: [(TokenType.SHOW, children: [(Float, 1.0, logo type: LogoType.FLOAT)])]), (StatementList, children: [(TokenType.SHOW, children: [(Float, 2.0, logo type: LogoType.FLOAT)])])])])])"
        ast = self.parser.parse(test_string)
        self.assertEqual(str(ast), expected)

    def test_bye(self):
        test_string = "bye"
        expected = "(Start, children: [(StatementList, children: [(TokenType.BYE)])])"
        ast = self.parser.parse(test_string)
        self.assertEqual(str(ast), expected)

    def test_bye_paren(self):
        test_string = "(bye)"
        expected = "(Start, children: [(StatementList, children: [(TokenType.BYE)])])"
        ast = self.parser.parse(test_string)
        self.assertEqual(str(ast), expected)

    def test_proc_call(self):
        test_string = "(foo)"
        expected = "(Start, children: [(StatementList, children: [(ProcCall, foo)])])"
        ast = self.parser.parse(test_string)
        self.assertEqual(str(ast), expected)

    def test_proc_call_as_part_of_something_else(self):
        test_string = "show (foo)"
        expected = "(Start, children: [(StatementList, children: [(TokenType.SHOW, children: [(ProcCall, foo)])])])"
        ast = self.parser.parse(test_string)
        self.assertEqual(str(ast), expected)

    def test_proc_call_with_args(self):
        test_string = "(foo 123)"
        expected = "(Start, children: [(StatementList, children: [(ProcCall, foo, children: [(Float, 123.0, logo type: LogoType.FLOAT)])])])"
        ast = self.parser.parse(test_string)
        self.assertEqual(str(ast), expected)

    def test_proc_call_with_args_as_part_of_something_else(self):
        test_string = "show (foo 123)"
        expected = "(Start, children: [(StatementList, children: [(TokenType.SHOW, children: [(ProcCall, foo, children: [(Float, 123.0, logo type: LogoType.FLOAT)])])])])"
        ast = self.parser.parse(test_string)
        self.assertEqual(str(ast), expected)
