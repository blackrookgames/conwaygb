__all__ = [\
    'CLIParseDef',]

from typing import\
    Any as _Any,\
    Callable as _Callable

class CLIParseDef:
    """
    Represents a definition for a handler for parsing input
    """

    #region init

    def __init__(self,\
            parse:None|_Callable[[str], tuple[bool, _Any]]):
        """
        Initializer for CLIParseDef
        
        :param parse:
            Function to use for parsing command-line input
        """
        self.__parse = parse

    #endregion

    #region properties

    @property
    def parse(self) -> None|_Callable[[str], tuple[bool, _Any]]:
        """
        Function to use for parsing command-line input
        """
        return self.__parse

    #endregion