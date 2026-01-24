from cli.CLIOption import *
from cli.CLIOptionFlagDef import *

class CLIOptionFlag(CLIOption):
    """
    Represents a command-line optional flag parameter
    """

    #region init

    def __init__(self,\
            varname:str,\
            paramdef:CLIOptionFlagDef):
        """
        Constructor for CLIOptionFlag

        :param varname:
            Variable name
        :param paramdef:
            Parameter definition
        """
        super().__init__(varname, paramdef)

    #endregion