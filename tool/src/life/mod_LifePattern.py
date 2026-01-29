__all__ = [\
    'LifePattern',]

import numpy as _np

from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil
from .mod_LifePatternRule import\
    LifePatternRule as _LifePatternRule

class LifePattern:
    """
    Represents a pattern in Conway's Game of Life
    """

    #region init

    def __init__(self,\
            width:int = 0,\
            height:int = 0,\
            rule:_LifePatternRule = _LifePatternRule()):
        """
        Initializer for LifePattern
        
        :param width:
            Pattern width (must be >= 0)
        :param height:
            Pattern height (must be >= 0)
        :raise ValueError:
            width is negative\n
            or\n
            height is negative
        """
        self.__setsize(width, height)
        self.__rule = rule

    #endregion

    #region operators

    def __len__(self):
        return len(self.__data)
    
    def __getitem__(self, key) -> _np.bool:
        try:
            index = self.__getindex(key)
            return self.__data[index]
        except Exception as _e:
            e = _e
        raise e
    
    def __setitem__(self, key, value):
        try:
            index = self.__getindex(key)
            self.__data[index] = _ErrorUtil.valid_bool(value)
            return
        except Exception as _e:
            e = _e
        raise e

    #endregion

    #region properties

    @property
    def width(self):
        """
        Pattern width
        """
        return self.__width

    @property
    def height(self):
        """
        Pattern height
        """
        return self.__height
    
    @property
    def rule(self):
        """
        Rule configuration
        """
        return self.__rule

    @rule.setter
    def rule(self, value:_LifePatternRule):
        self.__rule = value

    #endregion

    #region helper methods

    def __getindex(self, key):
        BADTUPLE = "Tuple must contain exactly 2 integers."
        # Is this a tuple?
        if isinstance(key, tuple):
            if not len(key) == 2:
                raise ValueError(BADTUPLE)
            x, y = key
            if not (isinstance(x, int) and isinstance(y, int)):
                raise ValueError(BADTUPLE)
            if x < 0 or x >= self.__width:
                raise ValueError("X-coordinate is out of range.")
            if y < 0 or y >= self.__height:
                raise ValueError("Y-coordinate is out of range.")
            return x + y * self.__width
        # Is this an integer?
        if isinstance(key, int):
            if key < 0 or key >= len(self.__data):
                raise ValueError("Index is out of range.")
            return key
        # Raise exception
        raise TypeError(f"{type(key).__name__} is not a supported key type.")

    def __setsize(self,\
            width:int,\
            height:int):
        if width < 0:
            raise ValueError("width cannot be negative.")
        if height < 0:
            raise ValueError("height cannot be negative.")
        self.__width = width
        self.__height = height
        self.__data = _np.zeros(self.__width * self.__height, dtype = bool)

    #endregion

    #region methods

    def resize(self,\
            width:int,\
            height:int,\
            preserve:bool = False):
        """
        Resizes the pattern
        
        :param width:
            Pattern width (must be >= 0)
        :param height:
            Pattern height (must be >= 0)
        :param preserve:
            Whether or not to preserve existing data
        :raise ValueError:
            width is negative\n
            or\n
            height is negative
        """
        prev_width = self.__width
        prev_height = self.__height
        prev_data = self.__data
        # Set size
        ex = None
        try: self.__setsize(width, height)
        except ValueError as _ex: ex = _ex
        if ex is not None: raise ex
        # Preserve (if requested)
        if preserve:
            min_width = min(prev_width, self.__width)
            min_height = min(prev_height, self.__height)
            curr = 0
            prev = 0
            for y in range(min_height):
                for x in range(min_width):
                    self.__data[curr + x] = prev_data[prev + x]
                curr += self.__width
                prev += prev_width

    #endregion