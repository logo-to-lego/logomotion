import unittest
from utils.code_generator import CodeGenerator
from entities.ast.node import Node
from entities.ast.logocommands import Move
from entities.ast.variables import Float
from lexer.token_types import TokenType


class CodegenTest(unittest.TestCase):


    def test_forward(self):
        node_float = Float(leaf = 100.0)
        node_fd = Move(node_type = TokenType.FD, children = [node_float])
        node_fd.generate_code()
        self.assertIn('double temp2 = 100.0;', node_fd._code_generator._code)
        self.assertIn('robot.travel(temp2);', node_fd._code_generator._code)

    def test_backwards(self):
        node_float = Float(leaf = 100.0)
        node_bk = Move(node_type = TokenType.BK, children = [node_float])
        node_bk.generate_code()
        self.assertIn('double temp1 = 100.0;', node_bk._code_generator._code)
        self.assertIn('robot.travel(-temp1);', node_bk._code_generator._code)

    def test_right_turn(self):
        node_float = Float(leaf = 100.0)
        node_rt = Move(node_type = TokenType.RT, children = [node_float])
        node_rt.generate_code()
        self.assertIn('double temp4 = 100.0;', node_rt._code_generator._code)
        self.assertIn('robot.rotate(-temp4);', node_rt._code_generator._code)

    def test_left_turn(self):
        node_float = Float(leaf = 100.0)
        node_lt = Move(node_type = TokenType.LT, children = [node_float])
        node_lt.generate_code()
        self.assertIn('double temp3 = 100.0;', node_lt._code_generator._code)
        self.assertIn('robot.rotate(temp3);', node_lt._code_generator._code)