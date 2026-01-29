__all__ = [\
    'LifePatternUtil',]

from ..img.mod_Img import\
    Img as _Img
from ..img.mod_ImgColor import\
    ImgColor as _ImgColor
from .mod_LifePattern import\
    LifePattern as _LifePattern

class LifePatternUtil:
    """
    Utility for patterns in Conway's Game of Life
    """

    #region img

    @classmethod
    def from_img(cls, img:_Img):
        """
        Creates a pattern using the specified image
        
        :param img:
            Input image
        :return:
            Created pattern
        """
        pattern = _LifePattern(\
            width = img.width,\
            height = img.height)
        for y in range(img.height):
            for x in range(img.width):
                pixel = img[x, y]
                pattern[x, y] = (pixel.r >= 128 and pixel.g >= 128 and pixel.b >= 128)
        # Return
        return pattern

    @classmethod
    def to_img(cls, pattern:_LifePattern):
        """
        Creates an image using the specified pattern\n
        Note that any rule configurations will be lost
        
        :param pattern:
            Input pattern
        :return:
            Created image
        """
        img = _Img(\
            width = max(1, pattern.width),
            height = max(1, pattern.height))
        LIVE = _ImgColor(r = 255, g = 255, b = 255)
        DEAD = _ImgColor()
        for y in range(pattern.height):
            for x in range(pattern.width):
                img[x, y] = LIVE if pattern[x, y] else DEAD
        # Return
        return img

    #endregion