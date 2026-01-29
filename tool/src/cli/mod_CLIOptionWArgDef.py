__all__ = [\
    'CLIOptionWArgDef',]

from typing import\
    Any as _Any,\
    Callable as _Callable

from .mod_CLIOptionDef import\
    CLIOptionDef as _CLIOptionDef
from .mod_CLIParseDef import\
    CLIParseDef as _CLIParseDef

class CLIOptionWArgDef(_CLIOptionDef, _CLIParseDef):
    """
    Represents a definition for a command-line optional parameter that takes an argument
    """

    #region init

    def __init__(self,\
            name:None|str = None,\
            short:None|str = None,\
            desc:None|str = None,\
            default:None|_Any = None,\
            parse:None|_Callable[[str], tuple[bool, _Any]] = None):
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
        _CLIOptionDef.__init__(self, name, short, desc, default)
        _CLIParseDef.__init__(self, parse)

    #endregion