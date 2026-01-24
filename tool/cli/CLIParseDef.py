from typing import Any, Callable

class CLIParseDef:
    """
    Represents a definition for a handler for parsing input
    """

    #region init

    def __init__(self,\
            parse:None|Callable[[str], tuple[bool, Any]]):
        """
        Initializer for CLIParseDef
        
        :param parse:
            Function to use for parsing command-line input
        """
        self.__parse = parse

    #endregion

    #region properties

    @property
    def parse(self) -> None|Callable[[str], tuple[bool, Any]]:
        """
        Function to use for parsing command-line input
        """
        return self.__parse

    #endregion