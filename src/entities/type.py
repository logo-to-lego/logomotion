"""Class that handles typing variables, when there are references to one another"""

from entities.logotypes import LogoType

class Type():
    """Type class stores the LogoType of a variable. The instance of this class
    can be then referenced to other variables which have the same LogoType"""
    def __init__(self, logotype: LogoType = LogoType.UNKNOWN):
        self._logotype = logotype

    @property
    def type(self):
        """Returns the LogoType enum of the Type class"""
        return self._logotype

    @type.setter
    def type(self, logotype: LogoType):
        if self._logotype == LogoType.UNKNOWN or self._logotype == LogoType.VOID:
            self._logotype = logotype
        else:
            raise Exception(f"LogoType was already defined as {self._logotype.value}")
