__all__ = [ 'ParseUtilStatus' ]

from enum import Enum, auto

class ParseUtilStatus(Enum):
    """
    Represents the return status of a parse operation
    """

    PASS = auto()
    """
    Input was successfully parsed
    """

    FAIL = auto()
    """
    Failed to parse input
    """

    TOLO = auto()
    """
    Parsed input is less than the allowed minimum
    """

    TOHI = auto()
    """
    Parsed input is greater than the allowed maximum
    """