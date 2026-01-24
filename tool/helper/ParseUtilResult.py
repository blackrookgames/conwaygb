from typing import Generic, TypeVar

from helper.ParseUtilStatus import *

T = TypeVar("T")
class ParseUtilResult(Generic[T]):
    """
    Represents the result of a parse operation
    """

    #region init

    def __init__(self,\
            status:ParseUtilStatus,\
            value:None|T):
        """
        Constructor for ParseUtilResult

        :param status:
            Return status
        :param value:
            Parsed value
        """
        self.__status = status
        self.__value = value

    @classmethod
    def passs(cls,\
            value:T):
        """
        Create a result indicating input parsed successfully

        :param value:
            Parsed value
        :return:
            Created result
        """
        return cls(ParseUtilStatus.PASS, value)

    @classmethod
    def fail(cls):
        """
        Create a result indicating input failed to parse

        :return:
            Created result
        """
        return cls(ParseUtilStatus.FAIL, None)
    
    @classmethod
    def tolo(cls):
        """
        Create a result indicating the parse value is too low

        :return:
            Created result
        """
        return cls(ParseUtilStatus.TOLO, None)
    
    @classmethod
    def tohi(cls):
        """
        Create a result indicating the parse value is too high

        :return:
            Created result
        """
        return cls(ParseUtilStatus.TOHI, None)

    #endregion

    #region properties

    @property
    def status(self) -> ParseUtilStatus:
        """
        Return status
        """
        return self.__status

    @property
    def value(self) -> None|T:
        """
        Return value
        """
        return self.__value

    #endregion