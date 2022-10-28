"""Code Generator module"""
from utils.logger import Logger, default_logger

START = "public class Logomotion { public static void main(string[] args) { "
END = "} }"
DEFAULT_NAME = "logomotion"


class CodeGenerator:
    """A class for generating code"""

    def __init__(self, name=DEFAULT_NAME, **dependencies):
        self._code = []
        self._name = name
        self._temp_var_index = 0
        self._logger: Logger = dependencies.get("logger", default_logger)

    def _increase_temp_var_index(self):
        """increase index for temp variables"""
        self._temp_var_index += 1
        return self._temp_var_index

    def _generate_temp_var(self):
        """create an unique temp variable name"""
        return f"temp{self._increase_temp_var_index()}"

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
    
    def binop(self, value1, value2, op):
        """create java code for binops and return variable name"""
        temp_var = self._generate_temp_var()
        code = f"double {temp_var} = {value1} {op} {value2};"
        self._logger.debug(code)
        self._code.append(code)
        return temp_var

    def write(self):
        """write a Java file"""
        try:
            with open(self._name + ".java", mode="w", encoding="utf-8") as file:
                file.write(START)
                for line in self._code:
                    file.write(line + " ")
                file.write(END)
                file.close()
        except Exception as error:
            print(f"An error occurred when writing {self._name}.java file:\n{error}")
            raise


default_code_generator = CodeGenerator()
