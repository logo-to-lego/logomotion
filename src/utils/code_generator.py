"""Code Generator module"""
import os
from utils.logger import Logger, default_logger

START = (
    "package logo; import classes.EV3MovePilot; "
    "public class Logo { public static void main(String[] args) { "
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
        self._code = []
        self._name = name
        self._temp_var_index = 0
        self._logger: Logger = dependencies.get("logger", default_logger)
        self._java_variables = dict()

    def _increase_temp_var_index(self):
        """increase index for temp variables"""
        self._temp_var_index += 1
        return self._temp_var_index

    def reset_temp_var_index(self):
        self._temp_var_index = 0

    def _generate_temp_var(self):
        """create an unique temp variable name"""
        return f"temp{self._increase_temp_var_index()}"

    def _generate_var(self):
        """Create a unique variable name"""
        return f"var{self._increase_temp_var_index()}"

    def _mangle_logo_var_name(self, logo_var_name):
        """Mangles logo variable names into Java variables. If the logo variable name was previously mangled, returns the previous one."""
        java_var_name = self._java_variables.get(logo_var_name, None)
        if not java_var_name:
            java_var_name = self._generate_var()
            self._java_variables[logo_var_name] = java_var_name
        return java_var_name

    def create_new_variable(self, logo_var_name, value_name):
        """Create a new Java variable and assign it a value."""
        java_var_name = self._mangle_logo_var_name(logo_var_name)
        line = f"var {java_var_name} = {value_name};"
        self._code.append(line)
        self._logger.debug(line)

    def move_forward(self, arg_var):
        """create Java code for moving forward"""
        line = f"robot.travel({arg_var});"
        self._code.append(line)
        self._logger.debug(line)

    def move_backwards(self, arg_var):
        """create Java code for moving backward"""
        line = f"robot.travel(-{arg_var});"
        self._code.append(line)
        self._logger.debug(line)

    def left_turn(self, arg_var):
        """create Java code for turning left"""
        line = f"robot.rotate({arg_var});"
        self._code.append(line)
        self._logger.debug(line)

    def right_turn(self, arg_var):
        """create Java code for turning right"""
        line = f"robot.rotate(-{arg_var});"
        self._code.append(line)
        self._logger.debug(line)

    def float(self, value):
        """create Java code for defining double variable with given value
        and return the variable name"""
        temp_var = self._generate_temp_var()
        code = f"double {temp_var} = {value};"
        self._logger.debug(code)
        self._code.append(code)
        return temp_var

    def boolean(self, value):
        """create Java code for defining boolean variable with given value
        and return the variable name"""
        temp_var = self._generate_temp_var()
        code = f"boolean {temp_var} = {value};"
        self._logger.debug(code)
        self._logger.append(code)
        return temp_var

    def binop(self, value1, value2, operation):
        """create java code for binops and return variable name"""
        temp_var = self._generate_temp_var()
        code = f"double {temp_var} = {value1} {operation} {value2};"
        self._logger.debug(code)
        self._code.append(code)
        return temp_var

    def relop(self, value1, value2, operation):
        """create java code for relops and return variable name"""
        temp_var = self._generate_temp_var()
        code = f"boolean {temp_var}  = {value1} {operation} {value2}"
        self._logger.debug(code)
        self._code.append(code)
        return temp_var

    def write(self):
        """write a Java file"""
        try:
            with open(PATH + self._name + ".java", mode="w+", encoding="utf-8") as file:
                file.write(START)
                for line in self._code:
                    file.write(line + " ")
                file.write(END)
                file.close()
        except Exception as error:
            print(f"An error occurred when writing {self._name}.java file:\n{error}")
            raise

    def get_generated_code(self):
        return self._code


default_code_generator = CodeGenerator()
