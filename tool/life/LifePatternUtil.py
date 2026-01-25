from numpy import uint64

class LifePatternUtil:
    """
    Utility for patterns in Conway's Game of Life
    """

    from img.Img import Img as __Img
    from img.ImgColor import ImgColor as __ImgColor
    from life.LifePattern import LifePattern as __LifePattern

    #region img

    @classmethod
    def from_img(cls, img:__Img):
        """
        Creates a pattern using the specified image
        
        :param img:
            Input image
        :return:
            Created pattern
        """
        pattern = cls.__LifePattern(\
            width = img.width,\
            height = img.height)
        for y in range(img.height):
            for x in range(img.width):
                pixel = img[x, y]
                pattern[x, y] = (pixel.r >= 128 and pixel.g >= 128 and pixel.b >= 128)
        # Return
        return pattern

    @classmethod
    def to_img(cls, pattern:__LifePattern):
        """
        Creates an image using the specified pattern\n
        Note that any rule configurations will be lost
        
        :param pattern:
            Input pattern
        :return:
            Created image
        """
        img = cls.__Img(\
            width = max(1, pattern.width),
            height = max(1, pattern.height))
        LIVE = cls.__ImgColor(r = 255, g = 255, b = 255)
        DEAD = cls.__ImgColor()
        for y in range(pattern.height):
            for x in range(pattern.width):
                img[x, y] = LIVE if pattern[x, y] else DEAD
        # Return
        return img

    #endregion