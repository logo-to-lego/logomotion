"""symbol module"""
from entities.logotypes import LogoType

class Symbol:
    "Class for symbol in symbol table"

    def __init__(self, name: str, logotype: LogoType, value=None, **kwargs):

        self._name = name
        if not isinstance(logotype, LogoType):
            raise TypeError("Symbols type must be an instance of LogoType Enum")
        self._type = logotype
        self._value = value

        # if more arguments are given
        for attribute, argument in kwargs.items():
            setattr(self, attribute, argument)

    @property
    def name(self):
        """get symbols name"""
        return self._name

    @property
    def value(self):
        """get symbols value"""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

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
        super().__init__(name, logotype, value, **kwargs)

    def __str__(self):
        return f"Variable {self._name}: type: {self._type.value}, value: {self._value}"

class Function(Symbol):
    "Class for functions in symbol table. Inherits Symbol class"

    def __init__(self, name, logotype=LogoType.VOID, value=None, args=None, **kwargs):
        """Constructor function for Function class

        Args:
            name (str): Functions name
            logotype (LogoType, optional): Functions return values type. Defaults to LogoType.VOID
            value (Any, optional): Functions return value. Defaults to None.
            args (list or tuple, optional): Arguments given to function. Defaults to None.
        """
        super().__init__(name, logotype, value, **kwargs)
        self._arguments = []
        if args:
            self._arguments.extend(args)

    def __str__(self):
        arg_str = ""
        if self._arguments:
            arg_str = f", arguments: {str(self._arguments)}"

        return f"Function {self._name}: type: {self._type.value}, value: {self._value}" + arg_str

    def get_function_argument(self, index: int):
        """get argument given to function within it's index"""
        if 0 <= index < len(self._arguments):
            return self._arguments[index]
        return None

    @property
    def arguments(self):
        """return functions arguments as list"""
        return self._arguments
