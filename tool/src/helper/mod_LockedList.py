__all__ = [ 'LockedList' ]

from typing import\
    Generic as _Generic,\
    TypeVar as _TypeVar

from .mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil

T = _TypeVar("T")
class LockedList(_Generic[T]):
    """
    Represents a list can't be directly modified
    """

    #region init

    def __init__(self, actual_list:list[T]):
        """
        Initializer for LockedList

        :param actual_list:
            (readonly) Actual list
        """
        self.__actual_list = actual_list

    #endregion

    #region operators

    def __len__(self):
        return len(self.__actual_list)

    def __getitem__(self, index):
        # Cast as integer
        _index = _ErrorUtil.valid_int(index, param = 'index')
        if _index < 0 or _index >= len(self.__actual_list):
            raise IndexError(f"index is out of range")
        # Return
        return self.__actual_list[_index]

    def __contains__(self, item):
        return item in self.__actual_list

    def __iter__(self):
        i = 0
        l = len(self.__actual_list)
        while i < l:
            yield self.__actual_list[i]
            i += 1

    #endregion