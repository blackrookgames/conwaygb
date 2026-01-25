from numpy import uint64
from sys import stderr

class GBUtil:
    """
    Utility for Gameboy-related operations
    """

    from cli.helper.IOUtil import IOUtil as __IOUtil
    from data.DataBuffer import DataBuffer as __DataBuffer
    from gb.GBTile import GBTile as __GBTile
    from gb.GBTile import GBTILE_SIZE as __GBTILE_SIZE

    #region tileset

    @classmethod
    def tileset_load(cls, path:str):
        """
        Attrmpts to load tileset data from a file
        
        :param path:
            Path of input file
        :return:
            List of tiles (or None if load failed)
        """
        # Create buffer
        buffer = cls.__IOUtil.buffer_load(path)
        if buffer is None:
            return None
        # Determine amount of tiles
        count = len(buffer) // cls.__GBTILE_SIZE
        # Load tiles
        tileset:list[GBUtil.__GBTile] = []
        for i in range(count):
            data0:uint64 = 0
            data1:uint64 = 0
            for j in range(cls.__GBTILE_SIZE // 2):
                data0 <<= 8
                data0 |= buffer.read_byte()
                data1 <<= 8
                data1 |= buffer.read_byte()
            tileset.append(cls.__GBTile(data0, data1))
        # Success!!!
        return tileset

    @classmethod
    def tileset_save(cls, tileset:list[__GBTile], path:str):
        """
        Attrmpts to save tileset data to a file
        
        :param tileset:
            List of tiles
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        # Create buffer
        buffer = cls.__DataBuffer(len(tileset) * cls.__GBTILE_SIZE)
        # Write tiles
        LEN = cls.__GBTILE_SIZE // 2
        for tile in tileset:
            shift = LEN * 8
            for j in range(LEN):
                shift -= 8
                buffer.write_byte(0xFF & (tile.data0 >> shift))
                buffer.write_byte(0xFF & (tile.data1 >> shift))
        # Save buffer
        return cls.__IOUtil.buffer_save(buffer, path)

    #endregion