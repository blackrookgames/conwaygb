__all__ = [\
    'GBTile',\
    'GBTILE_SIZE',]

from numpy import\
    uint64 as _uint64

GBTILE_SIZE = 16
"""
Size of a Game Boy tile (in bytes)
"""

class GBTile:
    """
    Represents a Game Boy tile
    """

    #region init

    def __init__(self, data0:_uint64, data1:_uint64):
        """
        Constructor for GBTile
        
        :param data0:
            Palette bit-0 value for each pixel
        :param data1:
            Palette bit-1 value for each pixel
        """
        self.__data0 = data0
        self.__data1 = data1

    #endregion

    #region operators

    def __repr__(self):
        return f"GBTile({self.__data0}, {self.__data1})"

    def __eq__(self, other):
        return self.__equals(other)
    
    def __ne__(self, other):
        return not self.__equals(other)
    
    def __hash__(self):
        return hash(self.__data0)

    def __str__(self):
        return f"{self.__data0:016X}, {self.__data1:016X}"

    #endregion

    #region properties

    @property
    def data0(self):
        """
        Palette bit-0 value for each pixel
        """
        return self.__data0
    
    @property
    def data1(self):
        """
        Palette bit-1 value for each pixel
        """
        return self.__data1

    #endregion

    #region helper methods

    def __equals(self, other):
        if not isinstance(other, GBTile):
            return False
        return self.__data0 == other.__data0 and self.__data1 == other.__data1
    
    #endregion