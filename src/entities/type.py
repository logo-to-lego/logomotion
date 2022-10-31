"""Class that handles typing variables, when there are references to one another"""

from entities.logotypes import LogoType
#from entities.symbol import Variable


class Type():
    """Type class stores the LogoType of a variable. The instance of this class
    can be then referenced to other variables which have the same LogoType"""

    def __init__(self, logotype: LogoType = LogoType.UNKNOWN, variables: set = {}): # variables is a set of Symbol objects
        self._logotype = logotype
        self._variables = variables

    @property
    def logotype(self):
        """Returns the LogoType enum of the Type class"""
        return self._logotype

    @property
    def variables(self):
        """Returns the variables of the type class"""
        return self._variables

    @logotype.setter
    def logotype(self, logotype: LogoType):
        if self._logotype == LogoType.UNKNOWN:
            self._logotype = logotype
        else:
            raise Exception(
                f"LogoType was already defined as {self._logotype.value}")

    def add_variable(self, var_symbol):
        self._variables.add(var_symbol)

    @staticmethod
    def concatenate(typeclass1: 'Type', typeclass2: 'Type') -> 'Type':
        if typeclass1.logotype != typeclass2.logotype:
            raise Exception(
                f"Logotypes do not match: {typeclass1.logotype.value} != {typeclass2.logotype.value}")

        vars = typeclass1.variables.union(typeclass2.variables)
        new_typeclass = Type(logotype=typeclass1.logotype, variables=vars)
        for var in vars:
            # update typeclass ref
            var.typeclass = new_typeclass

    def __str__(self) -> str:
        return f"LogoType: {self._logotype}, Variables: {self._variables}"
