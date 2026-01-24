from cli.CLIParam import *
from cli.CLIParse import *
from cli.CLIRequiredDef import *

class CLIRequired(CLIParam, CLIParse):
    """
    Represents a definition for a command-line required parameter
    """

    #region init

    def __init__(self,\
            varname:str,\
            paramdef:CLIRequiredDef):
        """
        Constructor for CLIRequired

        :param varname:
            Variable name
        :param paramdef:
            Parameter definition
        """
        CLIParam.__init__(self, varname, paramdef)
        CLIParse.__init__(self, paramdef)

    #endregion