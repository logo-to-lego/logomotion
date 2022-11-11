"""Code Generator module"""
# pylint: disable=too-many-public-methods
import os
from utils.logger import Logger, default_logger
from lexer.token_types import TokenType

START_METHOD = (
    "package logo; import classes.EV3MovePilot; import java.lang.Runnable;" \
    "public class Logo { "
)
START_MAIN = (
    "public static void main(String[] args) { " \
    "EV3MovePilot robot = new EV3MovePilot(5.6, 11.7); "
)
END = "} }"
DEFAULT_NAME = "Logo"
PATH = os.path.join(
    os.path.dirname(os.path.relpath(__file__)), "../../logomotion_gradle/src/main/java/logo/"
)


class CodeGenerator:
    """A class for generating Java code"""

    def __init__(self, name=DEFAULT_NAME, **dependencies):
        self._main = []
        self._method = []
        self._proc_flag = False
        self._name = name
        self._temp_var_index = 0
        self._logger: Logger = dependencies.get("logger", default_logger)
        self._java_variable_names = {}

    def _increase_temp_var_index(self):
        """increase index for temp variables"""
        self._temp_var_index += 1
        return self._temp_var_index

    def reset(self):
        """Resets code generator internals."""
        self._main = []
        self._java_variable_names = {}
        self._temp_var_index = 0
        self._method = []
        self._proc_flag = False

    def _append_code(self, code):
        if self._proc_flag:
            self._method.append(code)
        else:
            self._main.append(code)
        self._logger.debug(code)

    def start_function(self, name, type):
        if self._proc_flag:
            return
        self._proc_flag = True
        code = f"public {type} {name}("
        self._append_code(code)

    def end_function(self):
        if not self._proc_flag:
            return
        self._proc_flag = False
        code = "} "
        self._append_code(code)

    def _generate_temp_var(self):
        """create an unique temp variable name"""
        return f"temp{self._increase_temp_var_index()}"

    def _generate_var(self):
        """Create a unique variable name"""
        return f"var{self._increase_temp_var_index()}"

    def _mangle_logo_var_name(self, logo_var_name):
        """Mangles logo variable names into Java variables.
        If the logo variable name was previously mangled, returns the previous one."""
        java_var_name = self._java_variable_names.get(logo_var_name, None)
        if not java_var_name:
            java_var_name = self._generate_var()
            self._java_variable_names[logo_var_name] = java_var_name
        return java_var_name

    def create_new_variable(self, logo_var_name, value_name):
        """Create a new Java variable and assign it a value."""
        java_var_name = self._mangle_logo_var_name(logo_var_name)
        line = f"var {java_var_name} = {value_name};"
        self._code.append(line)
        self._logger.debug(line)

    def assign_value(self, logo_var_name, value_name):
        """Assign a new value to an already existing variable."""
        java_var_name = self._mangle_logo_var_name(logo_var_name)
        line = f"{java_var_name} = {value_name};"
        self._code.append(line)
        self._logger.debug(line)

    def variable_name(self, logo_var_name):
        """Returns the java variable name of the logo variable."""
        java_var_name = self._mangle_logo_var_name(logo_var_name)
        return java_var_name

    def move_forward(self, arg_var):
        """create Java code for moving forward"""
        code = f"robot.travel({arg_var});"
        self._append_code(code)

    def move_backwards(self, arg_var):
        """create Java code for moving backward"""
        code = f"robot.travel(-{arg_var});"
        self._append_code(code)

    def left_turn(self, arg_var):
        """create Java code for turning left"""
        code = f"robot.rotate({arg_var});"
        self._append_code(code)

    def right_turn(self, arg_var):
        """create Java code for turning right"""
        code = f"robot.rotate(-{arg_var});"
        self._append_code(code)

    def float(self, value):
        """create Java code for defining double variable with given value
        and return the variable name"""
        temp_var = self._generate_temp_var()
        code = f"double {temp_var} = {value};"
        self._append_code(code)
        return temp_var

    def boolean(self, value):
        """create Java code for defining boolean variable with given value
        and return the variable name"""
        temp_var = self._generate_temp_var()
        if value == TokenType.TRUE:
            value = "true"
        else:
            value = "false"
        code = f"boolean {temp_var} = {value};"
        self._append_code(code)
        return temp_var

    def string(self, value):
        temp_var = self._generate_temp_var()
        code = f'String {temp_var} = "{value}";'
        self._append_code(code)
        return temp_var

    def binop(self, value1, value2, operation):
        """create java code for binops and return variable name"""
        temp_var = self._generate_temp_var()
        code = f"double {temp_var} = {value1} {operation} {value2};"
        self._append_code(code)
        return temp_var

    def relop(self, value1, value2, operation):
        """create java code for relops and return variable name"""
        if operation == "<>":
            operation = "!="
        temp_var = self._generate_temp_var()
        code = f"boolean {temp_var} = {value1} {operation} {value2};"
        self._append_code(code)
        return temp_var

    def if_statement(self, conditional):
        """Create Java code to start an if statement in Java."""
        code = f"if ({conditional}) " + "{"
        self._append_code(code)

    def else_statement(self):
        """Create Java code to start an else statement in Java."""
        code = "else {"
        self._append_code(code)

    def closing_brace(self):
        """Generate a closing curly bracket"""
        code = "}"
        self._append_code(code)

    def if_statement_lambda(self, conditional, lambda_variable):
        """Create Java code for if statements utilising Java's lambda"""
        code = f"if ({conditional}) {lambda_variable}.run();"
        self._append_code(code)

    def lambda_no_param_start(self):
        """Generate the start of a paramless Java lambda, return lambda variable's name"""
        temp_var = self._generate_temp_var()
        code = f"Runnable {temp_var} = () -> " + "{"
        self._append_code(code)
        return temp_var

    def lambda_end(self):
        """Generate the closing bracket for Java lambda"""
        code = "};"
        self._append_code(code)

    def write(self):
        """write a Java file"""
        try:
            with open(PATH + self._name + ".java", mode="w+", encoding="utf-8") as file:
                file.write(START_METHOD)
                for method_line in self._method:
                    file.write(method_line + " ")
                file.write(START_MAIN)
                for line in self._main:
                    file.write(line + " ")
                file.write(END)
                file.close()
        except Exception as error:
            print(f"An error occurred when writing {self._name}.java file:\n{error}")
            raise

    def get_generated_code(self):
        return self._main


default_code_generator = CodeGenerator()
