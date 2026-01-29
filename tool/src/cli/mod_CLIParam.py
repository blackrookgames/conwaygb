__all__ = [\
    'CLIParam',]

from .mod_CLIParamDef import\
    CLIParamDef as _CLIParamDef

class CLIParam:
    """
    Represents a command-line parameter definition
    """

    #region init

    def __init__(self,\
            varname:str,\
            paramdef:_CLIParamDef):
        """
        Initializer for CLIParam

        :param varname:
            Variable name
        :param paramdef:
            Parameter definition
        """
        # name
        if paramdef.name is None:
            self.__name = varname
        else:
            self.__name = paramdef.name
        # desc
        self.__desc = paramdef.desc
    
    #endregion
    
    #region properties

    @property
    def name(self) -> str:
        """
        Parameter name
        """
        return self.__name

    @property
    def desc(self) -> None|str:
        """
        Parameter description
        """
        return self.__desc
    
    #endregion
    