"""symbol module"""
from entities.logotypes import LogoType


class Variable:
    "Class for symbol in symbol table"

    def __init__(self, name: str, logotype=LogoType.UNKNOWN):
        """Constructor function for Variable object

        Args:
            name (str): Variables name
            logotype (LogoType, optional): Variables values type. Defaults to LogoType.UNKNOWN.
        """
        self._name = name
        if not isinstance(logotype, LogoType):
            raise TypeError("Symbols type must be an instance of LogoType Enum")
        self._type = logotype

    @property
    def name(self):
        """get symbols name"""
        return self._name

    @property
    def type(self):
        """get symbols type"""
        return self._type

    @type.setter
    def type(self, logotype: LogoType):
        self._type = logotype

    def __str__(self):
        return f"Variable {self._name}: type: {self._type.value}"


class Function(Variable):
    "Class for functions in symbol table. Inherits Variable class"

    def __init__(self, name, params=None, logotype=LogoType.UNKNOWN):
        """Constructor function for Function class

        Args:
            name (str): Functions name
            params (dict, optional): Arguments given to function. Defaults to None.
            logotype (LogoType, optional): Functions return values type. Defaults to LogoType.VOID
        """
        super().__init__(name, logotype)
        if not params:
            self._parameters = {}
        else:
            self._parameters = params

    def __str__(self):
        params_str = ""
        if self._parameters:
            params_str = f", parameters: {str(self._parameters)}"
        return f"Function {self._name}: type: {self._type.value}" + params_str

    @property
    def parameters(self):
        """return functions arguments as list"""
        return self._parameters
