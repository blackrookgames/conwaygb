__all__ = [\
    'CLIParamCollectionParamDict',]

from typing import\
    Generic as _Generic,\
    TypeVar as _TypeVar

from .mod_CLIParam import\
    CLIParam as _CLIParam

T = _TypeVar("T", bound = _CLIParam)
class CLIParamCollectionParamDict(_Generic[T]):
    """
    Represents a dictionary of command-line parameters of a certain type
    """

    #region init

    def __init__(self, actual:dict[str, T]):
        """
        Initializer for CLIParamCollectionParamDict
        """
        self.__actual = actual

    #endregion

    #region operators

    def __len__(self):
        return len(self.__actual)

    def __getitem__(self, name):
        try:
            return self.__actual[name]
        except Exception as _ex:
            ex = _ex
        raise ex
    
    def __contains__(self, name):
        return name in self.__actual
    
    def __iter__(self):
        for entry in self.__actual.values():
            yield entry

    #endregion