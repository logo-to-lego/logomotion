"""Class that handles typing variables, when there are references to one another"""

from entities.logotypes import LogoType


class Type:
    """Type class stores the LogoType of a variable. The instance of this class
    can be then referenced to other variables which have the same LogoType"""

    def __init__(self, logotype: LogoType = LogoType.UNKNOWN):
        self._logotype = logotype

    @property
    def logotype(self):
        """Returns the LogoType enum of the Type class"""
        return self._logotype

    @logotype.setter
    def logotype(self, logotype: LogoType):
        if self._logotype == LogoType.UNKNOWN:
            self._logotype = logotype

    @staticmethod
    def concatenate(typeclass1: "Type", typeclass2: "Type") -> "Type":
        def get_new_logotype():
            if typeclass1.logotype != LogoType.UNKNOWN:
                return typeclass1.logotype
            if typeclass2.logotype != LogoType.UNKNOWN:
                return typeclass2.logotype
            return LogoType.UNKNOWN

        return Type(logotype=get_new_logotype())

    def __str__(self) -> str:
        string = (
            f"Typeclass {id(self)} LogoType: {self._logotype}")
        return string
