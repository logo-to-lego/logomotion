"""Types used in Logo. These types are used in symbol table type checks."""

from enum import Enum


class LogoType(Enum):
    """The types in Logo are String, Float, Boolean, Unknown and Void"""

    STRING = "STRING"
    FLOAT = "FLOAT"
    BOOL = "BOOL"
    VOID = "VOID"
    UNKNOWN = "UNKNOWN"
