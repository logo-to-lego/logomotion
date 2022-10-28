import unittest
from utils.code_generator import default_code_generator
from entities.ast.node import Node
from entities.ast.logocommands import Move
from entities.ast.variables import Float
from lexer.token_types import TokenType


class CodegenTest(unittest.TestCase):
    '''Test java code generation from nodes'''


    def tearDown(self):
        default_code_generator.reset_temp_var_index()

    def test_forward(self):
        node_float = Float(leaf = 100.0)
        node_fd = Move(node_type = TokenType.FD, children = [node_float])
        node_fd.generate_code()
        node_list = node_fd._code_generator._code
        self.assertIn('double temp1 = 100.0;', node_list)
        self.assertIn('robot.travel(temp1);', node_list)

    def test_backwards(self):
        node_float = Float(leaf = 100.0)
        node_bk = Move(node_type = TokenType.BK, children = [node_float])
        node_bk.generate_code()
        node_list = node_bk._code_generator._code
        self.assertIn('double temp1 = 100.0;', node_list)
        self.assertIn('robot.travel(-temp1);', node_list)

    def test_right_turn(self):
        node_float = Float(leaf = 100.0)
        node_rt = Move(node_type = TokenType.RT, children = [node_float])
        node_rt.generate_code()
        node_list = node_rt._code_generator._code
        self.assertIn('double temp1 = 100.0;', node_list)
        self.assertIn('robot.rotate(-temp1);', node_list)

    def test_left_turn(self):
        node_float = Float(leaf = 100.0)
        node_lt = Move(node_type = TokenType.LT, children = [node_float])
        node_lt.generate_code()
        node_list = node_lt._code_generator._code
        self.assertIn('double temp1 = 100.0;', node_list)
        self.assertIn('robot.rotate(temp1);', node_list)