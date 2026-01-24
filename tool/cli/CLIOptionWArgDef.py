from typing import Any, Callable

from cli.CLIOptionDef import *
from cli.CLIParseDef import *

class CLIOptionWArgDef(CLIOptionDef, CLIParseDef):
    """
    Represents a definition for a command-line optional parameter that takes an argument
    """

    #region init

    def __init__(self,\
            name:None|str = None,\
            short:None|str = None,\
            desc:None|str = None,\
            default:None|Any = None,\
            parse:None|Callable[[str], tuple[bool, Any]] = None):
        """
        Initializer for CLIOptionWArgDef
        
        :param name:
            Explicit name
        :param short:
            Shortcut
        :param desc:
            Description
        :param default:
            Default value if the user does not specify the optional parameter
        :param parse:
            Function to use for parsing command-line input
        """
        CLIOptionDef.__init__(self, name, short, desc, default)
        CLIParseDef.__init__(self, parse)

    #endregion