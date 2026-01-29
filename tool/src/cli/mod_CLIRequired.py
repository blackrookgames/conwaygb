__all__ = [\
    'CLIRequired',]

from .mod_CLIParam import\
    CLIParam as _CLIParam
from .mod_CLIParse import\
    CLIParse as _CLIParse
from .mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

class CLIRequired(_CLIParam, _CLIParse):
    """
    Represents a definition for a command-line required parameter
    """

    #region init

    def __init__(self,\
            varname:str,\
            paramdef:_CLIRequiredDef):
        """
        Initializer for CLIRequired

        :param varname:
            Variable name
        :param paramdef:
            Parameter definition
        """
        _CLIParam.__init__(self, varname, paramdef)
        _CLIParse.__init__(self, paramdef)

    #endregion