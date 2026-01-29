__all__ = [\
    'CLIOptionDef',]

from typing\
    import Any as _Any

from .mod_CLIParamDef import\
    CLIParamDef as _CLIParamDef

class CLIOptionDef(_CLIParamDef):
    """
    Represents a definition for a command-line optional parameter
    """

    #region init

    def __init__(self,
            name:None|str,\
            short:None|str,\
            desc:None|str,\
            default:None|_Any):
        """
        Initializer for CLIOptionDef
        
        :param name:
            Explicit name
        :param short:
            Shortcut
        :param desc:
            Description
        :param default:
            Default value if the user does not specify the optional parameter
        """
        super().__init__(name, desc)
        self.__short = short
        self.__default = default

    #endregion

    #region properties

    @property
    def short(self) -> None|str:
        """
        Shortcut
        """
        return self.__short

    @property
    def default(self) -> None|_Any:
        """
        Default value if the user does not specify the optional parameter
        """
        return self.__default
    
    #endregion
    