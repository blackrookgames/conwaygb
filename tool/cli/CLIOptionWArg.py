from cli.CLIOption import *
from cli.CLIOptionWArgDef import *
from cli.CLIParse import *

class CLIOptionWArg(CLIOption, CLIParse):
    """
    Represents a command-line optional parameter that takes an argument
    """

    #region init

    def __init__(self,\
            varname:str,\
            paramdef:CLIOptionWArgDef):
        """
        Constructor for CLIOptionWArg

        :param varname:
            Variable name
        :param paramdef:
            Parameter definition
        """
        CLIOption.__init__(self, varname, paramdef)
        CLIParse.__init__(self, paramdef)

    #endregion