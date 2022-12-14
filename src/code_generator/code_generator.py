"""Code Generator module"""
# pylint: disable=too-many-public-methods, too-many-instance-attributes
import os
from entities.logotypes import LogoType
from utils.logger import Logger, default_logger
from lexer.token_types import TokenType

START_METHOD = (
    "package logo; import classes.EV3MovePilot; import java.util.concurrent.Callable; \
    import classes.*;"

    "public class Logo { \
        EV3MovePilot robot; \
    public Logo() { \
        this.robot = new EV3MovePilot(); \
    }"
)

START_RUN = (
    "public void run() { "
)

END_RUN = "}"

START_MAIN = (
    "public static void main(String[] args) { "\
        "Logo logo = new Logo(); "\
        "logo.run();"
)
END = "} }"
DEFAULT_NAME = "Logo"
PATH = os.path.join(
    os.path.dirname(os.path.relpath(__file__)), "../../logomotion_gradle/src/main/java/logo/"
)
JAVA_TYPES = {
    LogoType.FLOAT: "DoubleVariable",
    LogoType.STRING: "StrVariable",
    LogoType.BOOL: "BoolVariable",
    LogoType.VOID: "void",
    LogoType.NAMELESS_FUNCTION: "CallableVariable"
}

JAVA_TYPES_OBJECTS = {
    LogoType.FLOAT : "Double",
    LogoType.STRING : "String",
    LogoType.BOOL : "Boolean"
}

class JavaCodeGenerator:
    """A class for generating Java code"""

    def __init__(self, name=DEFAULT_NAME, **dependencies):
        self._main = []
        self._method = []
        self._proc_flag = False
        self._name = name
        self._temp_var_index = 0
        self._logger: Logger = dependencies.get("logger", default_logger)
        self._preconf_funcs_dict = dependencies.get("funcs_dict", {})
        self._java_variable_names = {}
        self._java_function_names = {}

    def set_preconf_funcs_dict(self, pre_func_dict):
        # pylint: disable=W0201
        self._preconf_funcs_dict = pre_func_dict

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

    def start_function_declaration(self, logo_func_name, logo_func_type):
        if self._proc_flag:
            return
        self._proc_flag = True
        java_func_name = self._mangle_java_function_name(logo_func_name)
        code = f"public {JAVA_TYPES[logo_func_type]} {java_func_name}("
        self._append_code(code)

    def start_try_catch_block(self):
        code = "try {"
        self._append_code(code)

    def _mangle_java_function_name(self, logo_func_name):
        java_func_name = self._java_function_names.get(logo_func_name, None)
        if not java_func_name:
            java_func_name = self._generate_func_name()
            self._java_function_names[logo_func_name] = java_func_name
        return java_func_name

    def _generate_func_name(self):
        """create unique function name"""
        return f"func{self._increase_temp_var_index()}"

    def end_function_declaration(self):
        if not self._proc_flag:
            return
        code = "} "
        self._append_code(code)
        self._proc_flag = False

    def end_try_catch_block_in_procedure(self, logo_func_type):
        code = "} catch (ReturnException error) { "\
               f"return ({JAVA_TYPES[logo_func_type]}) error.returnValue;"\
               "}"
        self._append_code(code)

    def end_try_catch_block_outside_procedure(self):
        code = "} catch (ReturnException error) { "\
               "System.out.println(\"An unidentified error occurred.\");"\
               "}"
        self._append_code(code)

    def add_function_parameters(self, parameters):
        code = ""
        for index, param in enumerate(parameters):
            code += f"{JAVA_TYPES[param[0]]} {self._mangle_logo_var_name(param[1])}"
            if index < len(parameters) - 1:
                code += ", "
        code += ") {"
        self._append_code(code)

    def return_statement(self, arg_var):
        code = f"throw new ReturnException({arg_var});"
        self._append_code(code)

    def function_call(self, logo_func_name, arg_vars):
        java_func_name = self._mangle_java_function_name(logo_func_name)
        arguments = ", ".join(arg_vars)
        code = f"this.{java_func_name}({arguments});"
        self._append_code(code)

    def returning_function_call(self, logo_func_name, arg_vars):
        temp_var = self._generate_temp_var()
        java_func_name = self._mangle_java_function_name(logo_func_name)
        arguments = ", ".join(arg_vars)
        code = f"var {temp_var} = this.{java_func_name}({arguments});"
        self._append_code(code)
        return temp_var

    def returning_function_call_outside_procedure(self, logo_func_name, arg_vars, temp_var):
        java_func_name = self._mangle_java_function_name(logo_func_name)
        arguments = ", ".join(arg_vars)
        code = f"{temp_var} = this.{java_func_name}({arguments});"
        self._append_code(code)
        return temp_var

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

    def remove_java_variable_name(self, logo_var_name):
        if logo_var_name in self._java_variable_names:
            del self._java_variable_names[logo_var_name]
        else:
            print("Attempted to remove key that doesn't exist in code_generator,\
                remove_java_variable_name.")

    def create_new_variable(self, logo_var_name, value_name):
        """Create a new Java variable and assign it a value."""
        java_var_name = self._mangle_logo_var_name(logo_var_name)
        line = f"var {java_var_name} = {value_name};"
        self._append_code(line)

    def assign_value(self, logo_var_name, value_name):
        """Assign a new value to an already existing variable."""
        java_var_name = self._mangle_logo_var_name(logo_var_name)
        line = f"{java_var_name}.value = {value_name}.value;"
        self._append_code(line)

    def variable_name(self, logo_var_name):
        """Returns the java variable name of the logo variable."""
        java_var_name = self._mangle_logo_var_name(logo_var_name)
        temp_var = self._generate_temp_var()
        code = f"var {temp_var} = {java_var_name};"
        self._append_code(code)
        return temp_var

    def move_forward(self, arg_var):
        """create Java code for moving forward"""
        code = f"this.robot.travel({arg_var}.value);"
        self._append_code(code)

    def move_backwards(self, arg_var):
        """create Java code for moving backward"""
        code = f"this.robot.travel(-{arg_var}.value);"
        self._append_code(code)

    def left_turn(self, arg_var):
        """create Java code for turning left"""
        code = f"this.robot.rotate({arg_var}.value);"
        self._append_code(code)

    def right_turn(self, arg_var):
        """create Java code for turning right"""
        code = f"this.robot.rotate(-{arg_var}.value);"
        self._append_code(code)

    def show(self, arg_var):
        """create Java code for show"""
        code = f"System.out.println({arg_var}.value);"
        self._append_code(code)

    def bye(self):
        """create Java code for bye"""
        code = "System.exit(0);"
        self._append_code(code)

    def float(self, value):
        """create Java code for defining double variable with given value
        and return the variable name"""
        temp_var = self._generate_temp_var()
        code = f"DoubleVariable {temp_var} = new DoubleVariable({value});"
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
        code = f"BoolVariable {temp_var} = new BoolVariable({value});"
        self._append_code(code)
        return temp_var

    def string(self, value):
        temp_var = self._generate_temp_var()
        code = f'StrVariable {temp_var} = new StrVariable("{value}");'
        self._append_code(code)
        return temp_var

    def callable(self, value):
        temp_var = self._generate_temp_var()
        code = f"CallableVariable {temp_var} = new CallableVariable({value});"
        self._append_code(code)
        return temp_var

    def binop(self, value1, value2, operation):
        """create java code for binops and return variable name"""
        temp_var = self._generate_temp_var()
        #pylint: disable=c0301
        code = f"DoubleVariable {temp_var} = new DoubleVariable({value1}.value {operation} {value2}.value);"
        self._append_code(code)
        return temp_var

    def relop(self, value1, value2, operation):
        """create java code for relops and return variable name"""
        if operation == "<>":
            operation = "!="
        elif operation == "=":
            operation = "=="
        temp_var = self._generate_temp_var()
        # pylint: disable= C0301
        code = f"BoolVariable {temp_var} = new BoolVariable({value1}.value {operation} {value2}.value);"
        self._append_code(code)
        return temp_var

    def unary_op(self, value):
        """Create Java code for unaryops and return variable name"""
        temp_var = self._generate_temp_var()
        code = f"DoubleVariable {temp_var} = new DoubleVariable(-{value}.value);"
        self._append_code(code)
        return temp_var

    def if_statement(self, conditional):
        """Create Java code to start an if statement in Java."""
        code = f"if ({conditional}.value) " + "{"
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
        code = f"if ({conditional}.value) {lambda_variable}.value.call();"
        self._append_code(code)

    def lambda_no_param_start(self):
        """Generate the start of a paramless Java lambda, return lambda variable's name"""
        temp_var = self._generate_temp_var()
        code = f"Callable<Void> {temp_var} = () -> " + "{"
        self._append_code(code)
        return temp_var

    def lambda_param_start(self, param_name):
        """Generate the start of a parametered Java lambda, return lambda variable's name"""
        temp_var = self._generate_temp_var()
        java_param_name = self._mangle_logo_var_name(param_name)
        code = f"Consumer<DoubleVariable> {temp_var} = (DoubleVariable {java_param_name}) -> " + "{"
        self._append_code(code)
        return temp_var

    def lambda_end(self):
        """Generate the closing bracket for Java lambda"""
        code = "};"
        self._append_code(code)

    def return_null(self):
        """Return null at lambda end if proc type is void"""
        code = "return null;"
        self._append_code(code)

    def write(self, path=None):
        """write a Java file"""
        path = path if path is not None else PATH
        try:
            with open(path + self._name + ".java", mode="w+", encoding="utf-8") as file:
                file.write(START_METHOD)
                for fname in self._preconf_funcs_dict.keys():
                    file.write(self._preconf_funcs_dict[fname] + " ")
                for method_line in self._method:
                    file.write(method_line + " ")
                file.write(START_RUN)
                for line in self._main:
                    file.write(line + " ")
                file.write(END_RUN)
                file.write(START_MAIN)
                file.write(END)
                file.close()
        except Exception as error:
            print(f"An error occurred when writing {self._name}.java file:\n{error}")
            raise

    def get_generated_code(self):
        """Returns list of generated code for tests"""
        return self._method + self._main

    def _get_params_as_code_lines(self, path):
        params = []
        param_area = False
        with open(path, mode="r", encoding="utf-8") as file:
            for line in file.readlines():
                if "// Start params" in line:
                    param_area = True
                    continue
                if "// End params" in line:
                    param_area = False
                    continue
                if param_area:
                    params.append(line)
        return params

    def _create_params_as_code_lines(self, params, kwargs):
        for key, value in kwargs.items():
            search_key = f"this.{key} = "
            matches = [line for line in params if search_key in line]
            if len(matches) != 1:
                raise Exception(f"Either could not find '{key}' or there were more than one")

            line_to_modify = matches[0]

            if key in ("leftMotor", "rightMotor"):
                new_line = f"\t\t{search_key}new EV3LargeRegulatedMotor(MotorPort.{value});\n"
            else:
                new_line = f"\t\t{search_key}{value};\n"
            params = list(
                map(lambda x: x.replace(line_to_modify, new_line), params))  # pylint: disable=W0640
        return params

    def _write_new_params_to_file(self, path, param_lines):
        lines = []
        with open(path, mode="r", encoding="utf-8") as file:
            lines = file.readlines()

        param_area = False
        params_added = False
        with open(path, mode="w", encoding="utf-8") as file:
            for line in lines:
                if "// Start params" in line:
                    param_area = True
                    file.write(line)
                    continue
                if "// End params" in line:
                    param_area = False
                    file.write(line)
                    continue

                if param_area and not params_added:
                    for param_line in param_lines:
                        file.write(param_line)
                    params_added = True

                elif not param_area:
                    file.write(line)

    def add_env_variables(self, **kwargs):
        path = os.path.join(PATH, "../classes/EV3MovePilot.java")

        try:
            params = self._get_params_as_code_lines(path)
            param_lines = self._create_params_as_code_lines(params, kwargs)
            self._write_new_params_to_file(path, param_lines)

        except Exception as error:
            print("An error occurred when writing environment variables to EV3MovePilot.java")
            raise error


default_code_generator = JavaCodeGenerator()
