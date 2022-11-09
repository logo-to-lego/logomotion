"""Class that handles typing variables, when there are references to one another"""

from entities.logotypes import LogoType


class Type:
    """Type class stores the LogoType of a variable. The instance of this class
    can be then referenced to other variables which have the same LogoType"""

    def __init__(
        self, logotype: LogoType = LogoType.UNKNOWN, variables=None, functions=None
    ):  # variables is a set of Symbol objects
        self._logotype = logotype
        self._variables = variables if variables is not None else set()
        self._functions = functions if functions is not None else set()

    @property
    def logotype(self):
        """Returns the LogoType enum of the Type class"""
        return self._logotype

    @property
    def variables(self):
        """Returns the variables of the type class"""
        return self._variables

    @property
    def functions(self):
        """Returns the variables of the type class"""
        return self._functions

    @logotype.setter
    def logotype(self, logotype: LogoType):
        if self._logotype == LogoType.UNKNOWN:
            self._logotype = logotype
        else:
            raise Exception(f"LogoType was already defined as {self._logotype.value}")

    def add_variable(self, var_name):
        self._variables.add(var_name)

    def add_function(self, func_name):
        self._functions.add(func_name)

    @staticmethod
    def concatenate(typeclass1: "Type", typeclass2: "Type") -> "Type":
        logotype1 = typeclass1.logotype
        logotype2 = typeclass2.logotype

        def get_new_logotype():
            if logotype1 != LogoType.UNKNOWN:
                return logotype1
            if logotype2 != LogoType.UNKNOWN:
                return logotype2
            return LogoType.UNKNOWN

        variables = typeclass1.variables.union(typeclass2.variables)
        functions = typeclass1.functions.union(typeclass2.functions)
        return Type(logotype=get_new_logotype(), variables=variables, functions=functions)

    def __str__(self) -> str:
        string = (
            f"LogoType: {self._logotype}, Variables: "
            f"{self._variables}, Functions: {self._functions}"
        )
        return string
