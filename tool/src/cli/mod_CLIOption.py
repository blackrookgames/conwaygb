__all__ = [\
    'CLIOption',]

from typing\
    import Any as _Any

from .mod_CLIOptionDef import\
    CLIOptionDef as _CLIOptionDef
from .mod_CLIParam import\
    CLIParam as _CLIParam

class CLIOption(_CLIParam):
    """
    Represents a command-line optional parameter
    """

    #region init

    def __init__(self,\
            varname:str,\
            paramdef:_CLIOptionDef):
        """
        Initializer for CLIOption

        :param varname:
            Variable name
        :param paramdef:
            Parameter definition
        """
        super().__init__(varname, paramdef)
        self.__short = paramdef.short
        self.__default = paramdef.default
    
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