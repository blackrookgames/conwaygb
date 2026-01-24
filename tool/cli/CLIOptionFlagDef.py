from cli.CLIOptionDef import *

class CLIOptionFlagDef(CLIOptionDef):
    """
    Represents a definition for a command-line optional flag parameter
    """

    #region init

    def __init__(self,\
            name:None|str = None,\
            short:None|str = None,\
            desc:None|str = None):
        """
        Initializer for CLIOptionFlagDef
        
        :param name:
            Explicit name
        :param short:
            Shortcut
        :param desc:
            Description
        """
        super().__init__(name, short, desc, False)

    #endregion