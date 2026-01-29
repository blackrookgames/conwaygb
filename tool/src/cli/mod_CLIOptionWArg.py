__all__ = [\
    'CLIOptionWArg',]

from .mod_CLIOption import\
    CLIOption as _CLIOption
from .mod_CLIOptionWArgDef import\
    CLIOptionWArgDef as _CLIOptionWArgDef
from .mod_CLIParse import\
    CLIParse as _CLIParse

class CLIOptionWArg(_CLIOption, _CLIParse):
    """
    Represents a command-line optional parameter that takes an argument
    """

    #region init

    def __init__(self,\
            varname:str,\
            paramdef:_CLIOptionWArgDef):
        """
        Initializer for CLIOptionWArg

        :param varname:
            Variable name
        :param paramdef:
            Parameter definition
        """
        _CLIOption.__init__(self, varname, paramdef)
        _CLIParse.__init__(self, paramdef)

    #endregion