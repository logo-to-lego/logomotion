import unittest
from entities.logotypes import LogoType
from entities.symbol import Symbol, Variable, Function

class TestSymbol(unittest.TestCase):
    """test class for entities.symbol.Symbol and classes Variable
    and Function that inherits it"""

    def setUp(self):
        self.value1 = 123
        self.value2 = 456
        self.var = Variable("y", value=self.value1)
        self.func = Function("z", value=self.value2)
        print(self.var)
    
    def test_symbol_gives_right_name(self):
        given_name = "right_name"
        variable = Variable(given_name)
        self.assertEqual(variable.name, given_name)

    def test_symbols_default_logotypes_are_correct(self):
        self.assertEqual(self.var.type, LogoType.UNKNOWN.value)
        self.assertEqual(self.func.type, LogoType.VOID.value)

    def test_symbols_logotype_can_be_changed_with_setter(self):
        self.var.type = LogoType.FLOAT
        self.func.type = LogoType.FLOAT
        self.assertEqual(self.var.type, LogoType.FLOAT.value)
        self.assertEqual(self.func.type, LogoType.FLOAT.value)
    
    def test_symbols_value_can_be_changed_with_setter(self):
        self.var.value = self.value2
        self.func.value = self.value1
        self.assertEqual(self.var.value, self.value2)
        self.assertEqual(self.func.value, self.value1)
    
    def test_function_arguments_can_be_called(self):
        f = Function("z", args=[1,2,3])
        re1 = f.arguments[1]
        re2 = f.get_function_argument(1)
        self.assertEqual(re1, 2)
        self.assertEqual(re2, 2)
