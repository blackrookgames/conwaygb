from typing import Any, Callable

from cli.CLIParamDef import *
from cli.CLIParseDef import *

class CLIRequiredDef(CLIParamDef, CLIParseDef):
    """
    Represents a definition for a command-line required parameter
    """

    #region init

    def __init__(self,\
            name:None|str = None,\
            desc:None|str = None,\
            parse:None|Callable[[str], tuple[bool, Any]] = None):
        """
        Initializer for CLIRequiredDef
        
        :param name:
            Explicit name
        :param desc:
            Description
        :param parse:
            Function to use for parsing command-line input
        """
        CLIParamDef.__init__(self, name, desc)
        CLIParseDef.__init__(self, parse)

    #endregion