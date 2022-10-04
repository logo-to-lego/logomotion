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
        self.func = Function("z", params=[LogoType.FLOAT, LogoType.STRING])
    
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
    
    def test_variables_value_can_be_changed_with_setter(self):
        self.var.value = self.value2
        self.assertEqual(self.var.value, self.value2)
    
    def test_function_parameters_can_be_called(self):
        re1 = self.func.parameters[0]
        re2 = self.func.get_function_parameter(1)
        self.assertEqual(re1, LogoType.FLOAT)
        self.assertEqual(re2, LogoType.STRING)
    
    def test_get_function_parameter_with_invalid_index_gives_none(self):
        re1 = self.func.get_function_parameter(-1)
        re2 = self.func.get_function_parameter(2)
        self.assertEqual(re1, None)
        self.assertEqual(re2, None)

    def test_set_function_parameter_sets_parameter(self):
        i = 0
        re = self.func.set_function_parameter(LogoType.BOOL, i)
        self.assertEqual(re, True)
        self.assertEqual(self.func.parameters[i], LogoType.BOOL)
