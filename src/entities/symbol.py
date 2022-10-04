"""symbol module"""
from entities.logotypes import LogoType

class Symbol:
    "Class for symbol in symbol table"

    def __init__(self, name: str, logotype: LogoType, **kwargs):

        self._name = name
        if not isinstance(logotype, LogoType):
            raise TypeError("Symbols type must be an instance of LogoType Enum")
        self._type = logotype

        # if more arguments are given
        for attribute, argument in kwargs.items():
            setattr(self, attribute, argument)

    @property
    def name(self):
        """get symbols name"""
        return self._name

    @property
    def type(self):
        """get symbols type"""
        return self._type.value

    @type.setter
    def type(self, logotype: LogoType):
        self._type = logotype


class Variable(Symbol):
    "Class for variables in symbol table. Inherits Symbol class"

    def __init__(self, name, logotype=LogoType.UNKNOWN, value=None, **kwargs):
        """Constructor function for Variable object

        Args:
            name (str): Variables name
            logotype (LogoType, optional): Variables values type. Defaults to LogoType.UNKNOWN.
            value (_type_, optional): Variables value. Defaults to None.
        """
        super().__init__(name, logotype, **kwargs)
        self._value = value

    def __str__(self):
        return f"Variable {self._name}: type: {self._type.value}, value: {self._value}"

    @property
    def value(self):
        """get symbols value"""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class Function(Symbol):
    "Class for functions in symbol table. Inherits Symbol class"

    def __init__(self, name, logotype=LogoType.VOID, params=None, **kwargs):
        """Constructor function for Function class

        Args:
            name (str): Functions name
            logotype (LogoType, optional): Functions return values type. Defaults to LogoType.VOID
            args (list or tuple, optional): Arguments given to function. Defaults to None.
        """
        super().__init__(name, logotype, **kwargs)
        self._parameters = []
        if params:
            self._parameters.extend(params)

    def __str__(self):
        params_str = ""
        if self._parameters:
            params_str = f", parameters: {str(self._parameters)}"

        return f"Function {self._name}: type: {self._type.value}" + params_str

    def get_function_parameter(self, index: int):
        """get parameter given to function within it's index"""
        if 0 <= index < len(self._parameters):
            return self._parameters[index]
        return None

    def set_function_parameter(self, parameter, index: int):
        """set parameter to function"""
        if 0 <= index < len(self._parameters):
            self._parameters[index] = parameter
            return True
        return False

    @property
    def parameters(self):
        """return functions arguments as list"""
        return self._parameters
