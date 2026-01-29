__all__ = [\
    'CLIParamDef',]

class CLIParamDef:
    """
    Represents a definition for a command-line parameter
    """

    #region init

    def __init__(self,
            name:None|str,\
            desc:None|str):
        """
        Initializer for CLIParamDef
        
        :param name:
            Explicit name
        :param desc:
            Description
        """
        self.__name = name
        self.__desc = desc

    #endregion

    #region properties

    @property
    def name(self) -> None|str:
        """
        Explicit name
        """
        return self.__name

    @property
    def desc(self) -> None|str:
        """
        Description
        """
        return self.__desc
    
    #endregion
    