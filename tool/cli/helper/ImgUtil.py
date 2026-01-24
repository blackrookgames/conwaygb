from PIL import Image
from sys import stderr

from img.Img import *

class ImgUtil:
    """
    Utility for image operations
    """

    #region load

    @classmethod
    def load(cls, path:str):
        """
        Attempts to create an Img by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created Img (or None if load failed)
        """
        try: 
            with Image.open(path) as input:
                raw_w, raw_h = input.size
                img = Img(max(1, raw_w), max(1, raw_h))
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
                                    img[x, y] = ImgColor(\
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
                                img[x, y] = ImgColor(r = r, g = g, b = b, a = a)
            return img
        except Exception as e:
            print(f"ERROR: {e}", file = stderr)
            return None

    #endregion

    #region save

    @classmethod
    def save(cls, img:Img, path:str):
        """
        Attempts to save an Img to a file
        
        :param img:
            Img to save
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        output = Image.new('RGBA', (img.width, img.height))
        for y in range(img.height):
            for x in range(img.width):
                color = img[x, y]
                output.putpixel((x, y), (color.r, color.g, color.b, color.a))
        try:
            output.save(path)
            return True
        except Exception as e:
            print(f"ERROR: {e}", file = stderr)
            return False

    #endregion