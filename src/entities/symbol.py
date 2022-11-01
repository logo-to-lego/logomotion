"""symbol module"""
from entities.type import Type


class Variable:
    "Class for symbol in symbol table"

    def __init__(self, name: str, typeclass=Type()):
        """Constructor function for Variable object

        Args:
            name (str): Variables name
            typeclass (Type, optional): Class instance of variable values type.
                Defaults to new type class.
        """
        self._name = name
        if not isinstance(typeclass, Type):
            raise TypeError("Symbols type must be an instance of Type class")
        self._typeclass = typeclass

    @property
    def name(self):
        """get symbols name"""
        return self._name

    @property
    def typeclass(self):
        """get symbols type"""
        return self._typeclass

    @typeclass.setter
    def typeclass(self, typeclass: Type):
        self._typeclass = typeclass

    def __str__(self):
        return f"Variable {self._name}: Typeclass: ({self._typeclass})"


class Function(Variable):
    "Class for functions in symbol table. Inherits Variable class"

    def __init__(self, name, params=None, typeclass=Type()):
        """Constructor function for Function class

        Args:
            name (str): Functions name
            params (dict, optional): Arguments given to function. Defaults to None.
            typeclass (Type, optional): Functions return values type. Defaults to LogoType.UNKNOWN
        """
        super().__init__(name, typeclass)
        if not params:
            self._parameters = []
        else:
            self._parameters = params

    def __str__(self):
        params_str = ""
        if self._parameters:
            params_str = f", parameters: {str(self._parameters)}"
        return f"Function {self._name}: type: {self._typeclass.value}" + params_str

    @property
    def parameters(self):
        """return functions arguments as list"""
        return self._parameters
