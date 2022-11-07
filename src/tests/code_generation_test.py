import unittest
from utils.code_generator import default_code_generator
from entities.ast.node import Node
from entities.ast.logocommands import Move
from entities.ast.operations import RelOp
from entities.ast.variables import Float
from entities.ast.conditionals import If
from lexer.token_types import TokenType


class CodegenTest(unittest.TestCase):
    """Test java code generation from nodes"""

    def tearDown(self):
        default_code_generator.reset_temp_var_index()

    def test_forward(self):
        node_float = Float(leaf=100.0)
        node_fd = Move(node_type=TokenType.FD, children=[node_float])
        node_fd.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertIn("double temp1 = 100.0;", node_list)
        self.assertIn("robot.travel(temp1);", node_list)

    def test_backwards(self):
        node_float = Float(leaf=100.0)
        node_bk = Move(node_type=TokenType.BK, children=[node_float])
        node_bk.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertIn("double temp1 = 100.0;", node_list)
        self.assertIn("robot.travel(-temp1);", node_list)

    def test_right_turn(self):
        node_float = Float(leaf=100.0)
        node_rt = Move(node_type=TokenType.RT, children=[node_float])
        node_rt.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertIn("double temp1 = 100.0;", node_list)
        self.assertIn("robot.rotate(-temp1);", node_list)

    def test_left_turn(self):
        node_float = Float(leaf=100.0)
        node_lt = Move(node_type=TokenType.LT, children=[node_float])
        node_lt.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertIn("double temp1 = 100.0;", node_list)
        self.assertIn("robot.rotate(temp1);", node_list)

    def test_if_statement(self):
        node_float_1 = Float(leaf=1.0)
        node_float_2 = Float(leaf=2.0)
        node_relop = RelOp(leaf="<", children=[node_float_1,node_float_2])
        node_float_3 = Float(leaf=10.0)
        node_fd = Move(node_type=TokenType.FD, children=[node_float_3])
        node_if = If(leaf=node_relop, children=[node_fd])
        node_if.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertIn("boolean temp3 = temp1 < temp2;", node_list)
        self.assertIn("if (temp3) {", node_list)
        self.assertIn("double temp4 = 10.0;", node_list)
        self.assertIn("robot.travel(temp4);", node_list)
