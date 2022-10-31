import unittest
from entities.logotypes import LogoType
from entities.symbol import Variable, Function
from entities.symbol_table import SymbolTable


class TestType(unittest.TestCase):
    """test class for entities.symbol.Symbol and classes Variable
    and Function that inherits it"""

    def setUp(self):
        self.st = SymbolTable()
        self.st.insert("float1", Variable("float1"))
        self.st.insert("float2", Variable("float2"))
        self.st.insert("str1", Variable("str1"))
        self.st.insert("str2", Variable("str2"))

    def test_foo(self):
        pass
