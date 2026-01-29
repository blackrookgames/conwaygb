__all__ = [\
    'CLIParamCollection',]

from .mod_CLIOption import\
    CLIOption as _CLIOption
from .mod_CLIParam import\
    CLIParam as _CLIParam
from .mod_CLIParamCollectionParamDict import\
    CLIParamCollectionParamDict as _CLIParamCollectionParamDict
from .mod_CLIRequired import\
    CLIRequired as _CLIRequired
from ..helper.mod_LockedList import\
    LockedList as _LockedList

class CLIParamCollection:
    """
    Represents a collection of command-line parameters
    """

    #region init

    def __init__(self):
        """
        Initializer for CLIParamCollection
        """
        self.__col_params:dict[str, _CLIParam] = {}
        self.__col_reqparams:list[_CLIRequired] = []
        self.__col_optparams:dict[str, _CLIOption] = {}
        self.__col_shortcuts:dict[str, _CLIOption] = {}
        self.__reqparams:_LockedList[_CLIRequired] = _LockedList[_CLIRequired](self.__col_reqparams)
        self.__optparams:_CLIParamCollectionParamDict[_CLIOption] = _CLIParamCollectionParamDict[_CLIOption](self.__col_optparams)
        self.__shortcuts:_CLIParamCollectionParamDict[_CLIOption] = _CLIParamCollectionParamDict[_CLIOption](self.__col_shortcuts)

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
            param:_CLIRequired):
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
            param:_CLIOption):
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