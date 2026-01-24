from typing import Any

from cli.CLIOptionDef import *
from cli.CLIParam import *

class CLIOption(CLIParam):
    """
    Represents a command-line optional parameter
    """

    #region init

    def __init__(self,\
            varname:str,\
            paramdef:CLIOptionDef):
        """
        Constructor for CLIOption

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
    def default(self) -> None|Any:
        """
        Default value if the user does not specify the optional parameter
        """
        return self.__default
    
    #endregion