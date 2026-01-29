__all__ = [\
    'CLIOptionFlag',]

from .mod_CLIOption import\
    CLIOption as _CLIOption
from .mod_CLIOptionFlagDef import\
    CLIOptionFlagDef as _CLIOptionFlagDef

class CLIOptionFlag(_CLIOption):
    """
    Represents a command-line optional flag parameter
    """

    #region init

    def __init__(self,\
            varname:str,\
            paramdef:_CLIOptionFlagDef):
        """
        Initializer for CLIOptionFlag

        :param varname:
            Variable name
        :param paramdef:
            Parameter definition
        """
        super().__init__(varname, paramdef)

    #endregion