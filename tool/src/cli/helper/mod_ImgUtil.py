__all__ = [\
    'ImgUtil',]

from PIL import\
    Image as _Image
from sys import\
    stderr as _stderr

from ...img.mod_Img import\
    Img as _Img
from ...img.mod_ImgColor import\
    ImgColor as _ImgColor

class ImgUtil:
    """
    Utility for image operations
    """

    #region checkext

    @classmethod
    def checkext(cls, path:str):
        """
        Check if the path has a valid image file extension

        param path:
            Path
        return:
            Whether or not the path has a valid image file extension
        """
        return path.endswith((".png", ".bmp", ".jpg", ".tga", ".gif"))

    #endregion

    #region load

    @classmethod
    def load(cls, path:str):
        """
        Attempts to create an _Img by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created _Img (or None if load failed)
        """
        try: 
            with _Image.open(path) as input:
                raw_w, raw_h = input.size
                img = _Img(max(1, raw_w), max(1, raw_h))
                if input.mode == 'P':
                    # Get palette
                    palette = input.getpalette()
                    if len(palette) == 0: palette = None
                    # Loop thru pixels
                    for y in range(raw_h):
                        for x in range(raw_w):
                            raw_pixel = input.getpixel((x, y))
                            if isinstance(raw_pixel, int):
                                if palette is not None:
                                    offset = raw_pixel * 3
                                    img[x, y] = _ImgColor(\
                                        r = palette[offset],\
                                        g = palette[offset + 1],\
                                        b = palette[offset + 2])
                else:
                    # Loop thru pixels
                    for y in range(raw_h):
                        for x in range(raw_w):
                            raw_pixel = input.getpixel((x, y))
                            if isinstance(raw_pixel, tuple):
                                r = (0 if len(raw_pixel) == 0 else raw_pixel[0])
                                g = (0 if len(raw_pixel) <= 1 else raw_pixel[1])
                                b = (0 if len(raw_pixel) <= 2 else raw_pixel[2])
                                a = (0 if len(raw_pixel) <= 3 else raw_pixel[3])
                                img[x, y] = _ImgColor(r = r, g = g, b = b, a = a)
            return img
        except Exception as e:
            print(f"ERROR: {e}", file = _stderr)
            return None

    #endregion

    #region save

    @classmethod
    def save(cls, img:_Img, path:str):
        """
        Attempts to save an _Img to a file
        
        :param img:
            _Img to save
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        output = _Image.new('RGBA', (img.width, img.height))
        for y in range(img.height):
            for x in range(img.width):
                color = img[x, y]
                output.putpixel((x, y), (color.r, color.g, color.b, color.a))
        try:
            output.save(path)
            return True
        except Exception as e:
            print(f"ERROR: {e}", file = _stderr)
            return False

    #endregion