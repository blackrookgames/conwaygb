__all__ = [\
    'Img',]

import numpy as _np

from .mod_ImgColor import\
    ImgColor as _ImgColor

class Img:
    """
    Represents an image
    """

    #region init

    def __init__(self,\
            width:int = 1,\
            height:int = 1):
        """
        Initializer for Img
        
        :param width:
            Image width
        :param height:
            Image height
        :raise ValueError:
            width is less than or equal to zero\n
            or\n
            height is less than or equal to zero
        """
        ex = None
        try: self.__setsize(width, height)
        except ValueError as _ex: ex = _ex
        if ex is not None: raise ex

    #endregion

    #region operators

    def __len__(self):
        return len(self.__pixels)
    
    def __getitem__(self, key) -> _ImgColor:
        try:
            index = self.__getindex(key)
            return self.__pixels[index]
        except Exception as _e:
            e = _e
        raise e
    
    def __setitem__(self, key, value):
        try:
            index = self.__getindex(key)
            if not isinstance(value, _ImgColor):
                raise TypeError("Value must be a ImgColor.")
            self.__pixels[index] = value
            return
        except Exception as _e:
            e = _e
        raise e

    #endregion

    #region properties

    @property
    def width(self):
        """
        Image width
        """
        return self.__width

    @property
    def height(self):
        """
        Image height
        """
        return self.__height

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
            if key < 0 or key >= len(self.__pixels):
                raise ValueError("Index is out of range.")
            return key
        # Raise exception
        raise TypeError(f"{type(key).__name__} is not a supported key type.")

    def __setsize(self,\
            width:int,\
            height:int):
        if width <= 0:
            raise ValueError("width must be greater than zero.")
        if height <= 0:
            raise ValueError("height must be greater than zero.")
        self.__width = width
        self.__height = height
        self.__pixels = _np.full(self.__width * self.__height, _ImgColor(), dtype = object)

    #endregion

    #region methods

    def resize(self,\
            width:int,\
            height:int,\
            preserve:bool = False):
        """
        Docstring for resize
        
        :param width:
            Image width
        :param height:
            Image height
        :param preserve:
            Whether or not to preserve existing pixel data
        :raise ValueError:
            width is less than or equal to zero\n
            or\n
            height is less than or equal to zero
        """
        prev_width = self.__width
        prev_height = self.__height
        prev_pixels = self.__pixels
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
                    self.__pixels[curr + x] = prev_pixels[prev + x]
                curr += self.__width
                prev += prev_width

    #endregion