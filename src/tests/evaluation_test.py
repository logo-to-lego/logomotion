import unittest
from analysis.evaluation import Evaluation
from entities.symbol_table import SymbolTable
from parser.ast import *

class TestEvaluation(unittest.TestCase):
    """Test class for testing analysis.evaluation.Evaluation"""

    def setUp(self):
        self.st = SymbolTable()
        self.st.insert("x", 123)
        self.st.insert("y", "string")
        self.evaluation = Evaluation(self.st)

    def test_evaluation_method_returns_true_if_symbol_exists(self):
        node = Deref("x")
        ret = self.evaluation.semantic_checks["SA_SYMBOL_EXISTS"](node)
        self.assertTrue(ret)

    def test_evaluation_method_returns_false_if_symbol_does_not_exist(self):
        node = Deref("a")
        ret = self.evaluation.semantic_checks["SA_SYMBOL_EXISTS"](node)
        self.assertFalse(ret)

    def test_evaluation_method_does_not_add_to_errors_when_symbol_is_found(self):
        node = Deref("x")
        self.assertEqual(len(self.evaluation.semantic_errors), 0)
        self.evaluation.semantic_checks["SA_SYMBOL_EXISTS"](node)
        self.assertEqual(len(self.evaluation.semantic_errors), 0)

    def test_evaluation_method_adds_to_errors_when_symbol_is_not_found(self):
        node = Deref("a")
        self.assertEqual(len(self.evaluation.semantic_errors), 0)
        self.evaluation.semantic_checks["SA_SYMBOL_EXISTS"](node)
        self.assertEqual(len(self.evaluation.semantic_errors), 1)
        self.assertIn("Not Initialized", self.evaluation.semantic_errors[0])

    def test_evaluation_method_does_not_accept_non_deref_nodes(self):
        node = Number(17)
        self.assertRaises(Exception, self.evaluation.semantic_checks["SA_SYMBOL_EXISTS"], node)
