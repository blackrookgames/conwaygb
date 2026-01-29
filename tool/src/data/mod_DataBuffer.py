__all__ = [\
    'DataBuffer']

from .mod_DataError import\
    DataError as _DataError
from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil

class DataBuffer:
    """
    Represents a buffer containing byte data
    """

    #region init

    def __init__(self,\
            size:int = 0):
        if size < 0:
            raise ValueError("size must be greater than or equal to zero.")
        self.__data = bytearray(size)
        self.__cursor = 0

    #endregion

    #region operators

    def __len__(self):
        return len(self.__data)
    
    def __getitem__(self, index):
        try:
            return self.__data[self.__getindex(index)]
        except Exception as _e: e = _e
        raise e
    
    def __setitem__(self, index, value):
        try:
            _index = self.__getindex(index)
            self.__data[_index] = _ErrorUtil.valid_int(value, param = 'value')
            return
        except Exception as _e: e = _e
        raise e
    
    def __iter__(self):
        for _byte in self.__data:
            yield _byte

    #endregion

    #region properties

    @property
    def cursor(self):
        """
        Position of the cursor
        """
        return self.__cursor

    #endregion

    #region helper methods

    def __getindex(self, index):
        _index = _ErrorUtil.valid_int(index, param = 'index')
        if _index < 0 or _index >= len(self.__data):
            raise IndexError(f"index is out of range")
        return _index

    #endregion

    #region methods
    
    def set_cursor(self,\
            position:int,\
            raisedata:bool = False):
        """
        Sets the position of the cursor
        
        :param position:
            New position of the cursor
        :param raisedata:
            If true, an invalid cursor position will be raised as a DataError instead of a ValueError. 
            This may be useful for detecting files with invalid offset data.
        :raise ValueError:
            raisedata == False and the cursor position is invalid
        :raise DataError:
            raisedata == True and the cursor position is invalid
        """
        if position < 0 or position > len(self.__data):
            if raisedata:
                if position < 0:
                    raise _DataError("Offset cannot be below zero.")
                raise _DataError("Offset cannot exceed the length of the data.")
            raise ValueError("Cursor position must be between zero and the current length of the buffer.")
        self.__cursor = position
    
    def read_byte(self):
        """
        Reads a single byte from the buffer and increments the cursor by 1
        
        :return:
            Read value
        :raise DataError:
            Cursor is at the end of the buffer
        """
        if self.__cursor == len(self.__data):
            raise _DataError("Unexpected end of data.")
        value = self.__data[self.__cursor]
        self.__cursor += 1
        return value
    
    def write_byte(self,\
            value:int):
        """
        Writes a single byte to the buffer and increments the cursor by 1
        
        :param value:
            Value to write
        """
        if self.__cursor == len(self.__data):
            self.__data.append(value)
        else:
            self.__data[self.__cursor] = value
        self.__cursor += 1

    #endregion