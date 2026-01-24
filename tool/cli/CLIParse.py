from cli.CLIParseDef import *

class CLIParse:
    """
    Represents a handler for parsing input
    """

    #region init

    def __init__(self,\
            parsedef:CLIParseDef):
        """
        Initializer for CLIParse
        
        :param parsedef:
            Parse handler definition
        """
        self.__parse = parsedef.parse

    #endregion

    #region methods

    def parse(self, input:str) -> tuple[bool, Any]:
        """
        Attempts to parse some input
        
        :param input:
            Input to parse
        :return:
            tuple[bool, Any]\n
            bool: Whether or not the input was successfully parsed\n
            Any: Parsed value
        """
        if self.__parse is None:
            return True, input
        return self.__parse(input)

    #endregion