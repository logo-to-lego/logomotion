import unittest
from utils.code_generator import default_code_generator
from entities.ast.node import Node
from entities.ast.logocommands import Move
from entities.ast.operations import RelOp
from entities.ast.variables import Float
from entities.ast.variables import StringLiteral
from entities.ast.operations import BinOp
from entities.ast.operations import RelOp
from entities.ast.conditionals import If
from lexer.token_types import TokenType


class CodegenTest(unittest.TestCase):
    """Test java code generation from nodes"""

    def tearDown(self):
        default_code_generator.reset()

    def test_forward(self):
        node_float = Float(leaf=100.0)
        node_fd = Move(node_type=TokenType.FD, children=[node_float])
        node_fd.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("double temp1 = 100.0;", node_list[0])
        self.assertEqual("robot.travel(temp1);", node_list[1])

    def test_backwards(self):
        node_float = Float(leaf=100.0)
        node_bk = Move(node_type=TokenType.BK, children=[node_float])
        node_bk.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("double temp1 = 100.0;", node_list[0])
        self.assertEqual("robot.travel(-temp1);", node_list[1])

    def test_right_turn(self):
        node_float = Float(leaf=100.0)
        node_rt = Move(node_type=TokenType.RT, children=[node_float])
        node_rt.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("double temp1 = 100.0;", node_list[0])
        self.assertEqual("robot.rotate(-temp1);", node_list[1])

    def test_left_turn(self):
        node_float = Float(leaf=100.0)
        node_lt = Move(node_type=TokenType.LT, children=[node_float])
        node_lt.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("double temp1 = 100.0;", node_list[0])
        self.assertEqual("robot.rotate(temp1);", node_list[1])

    def test_binop(self):
        node_float1 = Float(leaf=1)
        node_float2 = Float(leaf=2)
        node_binoperation = BinOp(leaf="+", children=[node_float1, node_float2])
        node_binoperation.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("double temp1 = 1;", node_list[0])
        self.assertEqual("double temp2 = 2;", node_list[1])
        self.assertEqual("double temp3 = temp1 + temp2;", node_list[2])

    def test_boolean_float(self):
        node_float1 = Float(leaf=1)
        node_float2 = Float(leaf=1)
        node_boolean_op = RelOp(children=[node_float1, node_float2], leaf="=")
        node_boolean_op.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("double temp1 = 1;", node_list[0])
        self.assertEqual("double temp2 = 1;", node_list[1])
        self.assertEqual("boolean temp3 = temp1 = temp2;", node_list[2])

    def test_boolean_string(self):
        node_string1 = StringLiteral(leaf="sana")
        node_string2 = StringLiteral(leaf="anas")
        node_boolean_op = RelOp(children=[node_string1, node_string2], leaf="<>")
        node_boolean_op.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual('String temp1 = "sana";', node_list[0])
        self.assertEqual('String temp2 = "anas";', node_list[1])
        self.assertEqual("boolean temp3 = temp1 != temp2;", node_list[2])
