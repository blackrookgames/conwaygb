from numpy import uint64

class GBTileUtil:
    """
    Utility for Game Boy tiles
    """

    from img.Img import Img as __Img
    from img.ImgColor import ImgColor as __ImgColor
    from gb.GBTile import GBTile as __GBTile

    #region img

    @classmethod
    def from_img(cls, img:__Img):
        """
        Creates a tileset using the specified image
        
        :param img:
            Input image
        :return:
            List of tiles
        """
        # Tile count
        tcnt_x = img.width // 8
        tcnt_y = img.height // 8
        # Create tileset
        tileset:list[GBTileUtil.__GBTile] = []
        offy = 0
        for y in range(tcnt_y):
            offx = 0
            for x in range(tcnt_x):
                # Get tile data
                data0 = 0
                data1 = 0
                py = offy
                for yy in range(8):
                    px = offx
                    for xx in range(8):
                        # Get pixel
                        pixel = img[px, py]
                        value = int(round(((pixel.r + pixel.g + pixel.b) / 3) / 85))
                        # Update data
                        data0 <<= 1
                        data1 <<= 1
                        if (value & 0b01) == 0: data0 |= 1
                        if (value & 0b10) == 0: data1 |= 1
                        # Next
                        px += 1
                    py += 1
                # Add tile
                tileset.append(cls.__GBTile(data0, data1))
                # Next
                offx += 8
            offy += 8
        # Return
        return tileset

    @classmethod
    def to_img(cls, tileset:list[__GBTile], tilesperrow:int = 16):
        """
        Creates an image using the specified tileset
        
        :param tileset:
            Input tileset
        :return:
            Created image
        :raise ValueError:
            tilesperrow is less than 1
        """
        # Check tiles-per-row
        if tilesperrow < 1:
            raise ValueError("tilesperrow must be greater than or equal to 1.")
        # Row count
        rows = max(1, (len(tileset) + tilesperrow - 1) // tilesperrow) # Ensure there is at least one row
        # Create image
        BIT = 1 << 63
        img = cls.__Img(tilesperrow * 8, rows * 8)
        for i in range(len(tileset)):
            tile = tileset[i]
            offx = (i % tilesperrow) * 8
            offy = (i // tilesperrow) * 8
            # Set pixel data
            data0 = tile.data0
            data1 = tile.data1
            py = offy
            for y in range(8):
                px = offx
                for x in range(8):
                    # Compute pixel
                    value = 0
                    if (data0 & BIT) == 0: value |= 0b01
                    if (data1 & BIT) == 0: value |= 0b10
                    value *= 85
                    img[px, py] = cls.__ImgColor(r = value, g = value, b = value)
                    # Next pixel
                    data0 <<= 1
                    data1 <<= 1
                    # Next
                    px += 1
                py += 1
        # Return
        return img

    #endregion