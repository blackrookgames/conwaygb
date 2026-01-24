from cli.CLIOptionFlag import *
from cli.CLIOptionWArg import *
from cli.CLIParamCollectionParamDict import *
from cli.CLIRequired import *
from helper.LockedList import *

class CLIParamCollection:
    """
    Represents a collection of command-line parameters
    """

    #region init

    def __init__(self):
        """
        Initializer for CLIParamCollection
        """
        self.__col_params:dict[str, CLIParam] = {}
        self.__col_reqparams:list[CLIRequired] = []
        self.__col_optparams:dict[str, CLIOption] = {}
        self.__col_shortcuts:dict[str, CLIOption] = {}
        self.__reqparams:LockedList[CLIRequired] = LockedList[CLIRequired](self.__col_reqparams)
        self.__optparams:CLIParamCollectionParamDict[CLIOption] = CLIParamCollectionParamDict[CLIOption](self.__col_optparams)
        self.__shortcuts:CLIParamCollectionParamDict[CLIOption] = CLIParamCollectionParamDict[CLIOption](self.__col_shortcuts)

    #endregion

    #region operators

    def __len__(self):
        return len(self.__col_params)

    def __getitem__(self, name):
        try:
            return self.__col_params[name]
        except Exception as _ex:
            ex = _ex
        raise ex
    
    def __contains__(self, name):
        return name in self.__col_params
    
    def __iter__(self):
        for entry in self.__col_params.values():
            yield entry

    #endregion

    #region properties

    @property
    def reqparams(self):
        """
        List of required parameters
        """
        return self.__reqparams
    
    @property
    def optparams(self):
        """
        Dictionary of optional parameters, keyed by parameter name
        """
        return self.__optparams
    
    @property
    def shortcuts(self):
        """
        Dictionary of optional parameters containing shortcuts, keyed by parameter shortcut
        """
        return self.__shortcuts

    #endregion

    #region methods

    def add_reqparam(self,\
            param:CLIRequired):
        """
        Attempts to add the specified required parameter
        
        :param param:
            Parameter to add
        :return:
            Whether or not successful
        """
        if param.name in self.__col_params:
            return False
        self.__col_params[param.name] = param
        self.__col_reqparams.append(param)
        return True

    def add_optparam(self,\
            param:CLIOption):
        """
        Attempts to add the specified optional parameter
        
        :param param:
            Parameter to add
        :return:
            Whether or not successful
        """
        if param.name in self.__col_params:
            return False
        self.__col_params[param.name] = param
        self.__col_optparams[param.name] = param
        if param.short is not None and (not (param.short in self.__col_shortcuts)):
            self.__col_shortcuts[param.short] = param
        return True

    #endregion