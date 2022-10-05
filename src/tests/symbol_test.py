from logging import exception
import unittest
from entities.logotypes import LogoType
from entities.symbol import Variable, Function

class TestSymbol(unittest.TestCase):
    """test class for entities.symbol.Symbol and classes Variable
    and Function that inherits it"""

    def setUp(self):
        self.value1 = 123
        self.value2 = 456
        self.var = Variable("x", )
        self.func = Function("f", params={"x": LogoType.FLOAT, "y": LogoType.STRING})

    def test_symbol_gives_right_name(self):
        given_name = "right_name"
        variable = Variable(given_name)
        self.assertEqual(variable.name, given_name)

    def test_symbols_default_logotypes_are_correct(self):
        self.assertEqual(self.var.type, LogoType.UNKNOWN.value)
        self.assertEqual(self.func.type, LogoType.UNKNOWN.value)

    def test_symbols_logotype_can_be_changed_with_setter(self):
        self.var.type = LogoType.FLOAT
        self.func.type = LogoType.FLOAT
        self.assertEqual(self.var.type, LogoType.FLOAT.value)
        self.assertEqual(self.func.type, LogoType.FLOAT.value)

    def test_variables_value_can_be_changed_with_setter(self):
        self.var.value = self.value2
        self.assertEqual(self.var.value, self.value2)

    def test_function_parameters_can_be_called(self):
        re1 = self.func.parameters["x"]
        self.assertEqual(re1, LogoType.FLOAT)

    def test_wrong_type_for_logotype_parameter_raises_type_error(self):
        with self.assertRaises(TypeError):
            Variable("name", "float")

    def test_empty_argument_for_params_forms_empty_dict(self):
        f = Function("name")
        re = f.parameters
        self.assertDictEqual(re, {})
