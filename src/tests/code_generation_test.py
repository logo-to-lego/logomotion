import unittest
from entities.ast.statementlist import StatementList
from code_generator.code_generator import default_code_generator
from entities.ast.node import Node
from entities.ast.logocommands import Bye, Make, Move, Show
from entities.ast.variables import Deref, Float, StringLiteral
from entities.ast.logocommands import Move
from entities.ast.operations import RelOp
from entities.ast.variables import Float
from entities.ast.variables import StringLiteral
from entities.ast.operations import BinOp
from entities.ast.operations import RelOp
from entities.ast.operations import UnaryOp
from entities.ast.conditionals import If
from entities.ast.unknown_function import UnknownFunction
from entities.ast.functions import ProcCall, ProcDecl, ProcArgs, ProcArg
from entities.logotypes import LogoType
from entities.symbol import Function, Variable
from entities.type import Type
from lexer.token_types import TokenType
from entities.symbol_table import default_variable_table, default_function_table
from entities.preconfigured_functions import initialize_logo_functions


class CodegenTest(unittest.TestCase):
    """Test java code generation from nodes"""

    def setUp(self):
        default_code_generator.reset()
        default_variable_table.reset()
        default_function_table.reset()
        self.function_table = initialize_logo_functions(default_function_table)

    def tearDown(self):
        default_code_generator.reset()
        default_variable_table.reset()
        default_function_table.reset()

    def test_forward(self):
        node_float = Float(leaf=100.0)
        node_fd = Move(node_type=TokenType.FD, children=[node_float])
        node_fd.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("DoubleVariable temp1 = new DoubleVariable(100.0);", node_list[0])
        self.assertEqual("this.robot.travel(temp1.value);", node_list[1])

    def test_backwards(self):
        node_float = Float(leaf=100.0)
        node_bk = Move(node_type=TokenType.BK, children=[node_float])
        node_bk.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("DoubleVariable temp1 = new DoubleVariable(100.0);", node_list[0])
        self.assertEqual("this.robot.travel(-temp1.value);", node_list[1])

    def test_right_turn(self):
        node_float = Float(leaf=100.0)
        node_rt = Move(node_type=TokenType.RT, children=[node_float])
        node_rt.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("DoubleVariable temp1 = new DoubleVariable(100.0);", node_list[0])
        self.assertEqual("this.robot.rotate(-temp1.value);", node_list[1])

    def test_left_turn(self):
        node_float = Float(leaf=100.0)
        node_lt = Move(node_type=TokenType.LT, children=[node_float])
        node_lt.generate_code()
        code_list = default_code_generator.get_generated_code()
        self.assertEqual("DoubleVariable temp1 = new DoubleVariable(100.0);", code_list[0])
        self.assertEqual("this.robot.rotate(temp1.value);", code_list[1])

    def test_make(self):
        node_float = Float(leaf=10.0)
        node_name = StringLiteral(leaf="turn.angle")
        node_make = Make(leaf=node_name, children=[node_float])
        node_make.check_types()
        node_make.generate_code()
        code_list = default_code_generator.get_generated_code()
        self.assertEqual("DoubleVariable temp1 = new DoubleVariable(10.0);", code_list[0])
        self.assertEqual("var var2 = temp1;", code_list[1])

    def test_make_with_deref(self):
        node_float = Float(leaf=19.0)
        node_b_name = StringLiteral(leaf="turn.angle")
        node_make_b = Make(leaf=node_b_name, children=[node_float])
        node_b_deref = Deref(leaf="turn.angle")
        node_a_name = StringLiteral(leaf="other.angle")
        node_make_a = Make(leaf=node_a_name, children=[node_b_deref])
        nodes = StatementList(children=[node_make_b, node_make_a])
        nodes.check_types()
        nodes.generate_code()
        code_list = default_code_generator.get_generated_code()
        self.assertEqual("DoubleVariable temp1 = new DoubleVariable(19.0);", code_list[0])
        self.assertEqual("var var2 = temp1;", code_list[1])
        self.assertEqual("var temp3 = var2;", code_list[2])

    def test_assign_value_to_existing(self):
        node_float = Float(leaf=3)
        node_a_name = StringLiteral(leaf="a_variable")
        node_make_a = Make(leaf=node_a_name, children=[node_float])
        node_float_2nd = Float(leaf=4)
        node_make_b = Make(leaf=node_a_name, children=[node_float_2nd])
        nodes = StatementList(children=[node_make_a, node_make_b])
        nodes.check_types()
        nodes.generate_code()
        code_list = default_code_generator.get_generated_code()
        self.assertEqual("DoubleVariable temp1 = new DoubleVariable(3);", code_list[0])
        self.assertEqual("var var2 = temp1;", code_list[1])
        self.assertEqual("DoubleVariable temp3 = new DoubleVariable(4);", code_list[2])
        self.assertEqual("var2.value = temp3.value;", code_list[3])
    
    def test_for_make(self):
        node_str = StringLiteral(leaf="yksi")
        node_float_start = Float(leaf=0)
        node_float_limit = Float(leaf=5)
        node_float_step = Float(leaf=1)
        node_str_2 = StringLiteral(leaf="kaksi")
        node_float_yksi = Float(leaf=1)
        node_make_a = Make(leaf=node_str_2, children=[node_float_yksi])
        node_nameless = UnknownFunction(children=[StatementList(children=[node_make_a])], iter_param=node_str)
        node_proccall = ProcCall(leaf="for", children=[node_str, node_float_start, \
            node_float_limit, node_float_step, node_nameless])
        nodes = StatementList(children=[node_proccall])
        nodes.check_types()
        nodes.generate_code()
        code_list = default_code_generator.get_generated_code()
        self.assertEqual("""StrVariable temp1 = new StrVariable("yksi");""", code_list[0])
        self.assertEqual("DoubleVariable temp2 = new DoubleVariable(0);", code_list[1])
        self.assertEqual("DoubleVariable temp3 = new DoubleVariable(5);", code_list[2])
        self.assertEqual("DoubleVariable temp4 = new DoubleVariable(1);", code_list[3])
        self.assertEqual("Callable<Void> temp5 = () -> {", code_list[4])
        self.assertEqual("DoubleVariable temp6 = new DoubleVariable(1);", code_list[5])
        self.assertEqual("var var7 = temp6;", code_list[6])
        self.assertEqual("this.func9(temp1, temp2, temp3, temp4, temp8);", code_list[11])
        
    
    def test_binop(self):
        node_float1 = Float(leaf=1)
        node_float2 = Float(leaf=2)
        node_binoperation = BinOp(leaf="+", children=[node_float1, node_float2])
        node_binoperation.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("DoubleVariable temp1 = new DoubleVariable(1);", node_list[0])
        self.assertEqual("DoubleVariable temp2 = new DoubleVariable(2);", node_list[1])
        self.assertEqual("DoubleVariable temp3 = new DoubleVariable(temp1.value + temp2.value);", node_list[2])

    def test_unop(self):
        node_float = Float(leaf=1)
        node_unop = UnaryOp(leaf="-", children=[node_float])
        node_unop.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("DoubleVariable temp1 = new DoubleVariable(1);", node_list[0])
        self.assertEqual("DoubleVariable temp2 = new DoubleVariable(-temp1.value);", node_list[1])

    def test_boolean_float(self):
        node_float1 = Float(leaf=1)
        node_float2 = Float(leaf=1)
        node_boolean_op = RelOp(children=[node_float1, node_float2], leaf="=")
        node_boolean_op.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("DoubleVariable temp1 = new DoubleVariable(1);", node_list[0])
        self.assertEqual("DoubleVariable temp2 = new DoubleVariable(1);", node_list[1])
        self.assertEqual("BoolVariable temp3 = new BoolVariable(temp1.value == temp2.value);", node_list[2])

    def test_boolean_string(self):
        node_string1 = StringLiteral(leaf="sana")
        node_string2 = StringLiteral(leaf="anas")
        node_boolean_op = RelOp(children=[node_string1, node_string2], leaf="<>")
        node_boolean_op.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual('StrVariable temp1 = new StrVariable("sana");', node_list[0])
        self.assertEqual('StrVariable temp2 = new StrVariable("anas");', node_list[1])
        self.assertEqual("BoolVariable temp3 = new BoolVariable(temp1.value != temp2.value);", node_list[2])

    def test_void_function_call(self):
        node_function = ProcCall(leaf="test", children=None)
        node_function.procedure = Function(name="test", typeclass=Type(logotype=LogoType.VOID))
        node_function.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("this.func2();", node_list[0])

    def test_non_void_function_call(self):
        node_function = ProcCall(leaf="test", children=None)
        node_function.procedure = Function(name="test", typeclass=Type(logotype=LogoType.FLOAT))
        node_function.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("var temp1 = this.func2();", node_list[0])

    def test_make_leaf_is_case_insensitive(self):
        node_float1 = Float(leaf=1.0)
        node_float2 = Float(leaf=2.0)
        node_name1 = StringLiteral(leaf="Test")
        node_name2 = StringLiteral(leaf="tEST")
        node_make1 = Make(children=[node_float1], leaf=node_name1)
        node_make2 = Make(children=[node_float2], leaf=node_name2)
        nodes = StatementList(children=[node_make1, node_make2])
        nodes.check_types()
        nodes.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("var var2 = temp1;", node_list[1])
        self.assertEqual("var2.value = temp3.value;", node_list[3])

    def test_variables_are_case_insensitive(self):
        node_float = Float(leaf=1.0)
        node_name1 = StringLiteral(leaf="Test1")
        node_name2 = StringLiteral(leaf="Test2")
        node_make1 = Make(children=[node_float], leaf=node_name1)
        node_make2 = Make(children=[Deref(leaf="tEST1")], leaf=node_name2)
        nodes = StatementList(children=[node_make1, node_make2])
        nodes.check_types()
        nodes.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("var var2 = temp1;", node_list[1])
        self.assertEqual("var temp3 = var2;", node_list[2])

    def test_show(self):
        node_float = Float(leaf=4.2)
        node_str = StringLiteral(leaf="kissa")
        node_function = Show(node_type=TokenType.SHOW, children=[node_float, node_str])
        node_function.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("DoubleVariable temp1 = new DoubleVariable(4.2);", node_list[0])
        self.assertEqual("System.out.println(temp1.value);", node_list[1])
        self.assertEqual("StrVariable temp2 = new StrVariable(\"kissa\");", node_list[2])
        self.assertEqual("System.out.println(temp2.value);", node_list[3])

    def test_bye(self):
        node_function = Bye(node_type=TokenType.BYE, children=[])
        node_function.generate_code()
        node_list = default_code_generator.get_generated_code()
        self.assertEqual("System.exit(0);", node_list[0])
