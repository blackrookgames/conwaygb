import numpy as np
import sys

from typing import cast

import src.cli as cli
import src.gb as gb
import src.data as data
import src.img as img

TILESIZE = 8
TILEDIM = 32

class cmd_menu(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Creates a menu tilemap from an image."

    #region required

    __input = cli.CLIRequiredDef(\
        name = "input",\
        desc = "Path to the input file")
    __output = cli.CLIRequiredDef(\
        name = "output",\
        desc = "Path to the output *.bin file")
    __tileset = cli.CLIRequiredDef(\
        name = "tileset",\
        desc = "Path to the tileset file")

    #endregion

    #region helper methods

    @classmethod
    def __occurbyfreq(cls, buffer:data.DataBuffer):
        """
        Byte values are sorted by frequency (least->most) and value (greatest->least).
        This allows values like 0xFF and 0xFE to be placed at the front if they're less frequent.
        """
        # Get occurances
        occ_value = np.arange(256, dtype = np.uint8)
        occ_count = np.zeros(256, dtype = np.uint64)
        for _b in buffer:
            occ_count[_b] += 1
        # Sort by frequencies
        for _i in range(len(occ_value) - 1):
            for _j in range(len(occ_value) - 1):
                _v0 = occ_value[_j]
                _c0 = occ_count[_j]
                _v1 = occ_value[_j + 1]
                _c1 = occ_count[_j + 1]
                # Compare
                if _c0 < _c1: continue
                if _c0 == _c1 and _v0 >= _v1: continue # Allow higher values to be placed in front (Example: 5, 4, 3, 2)
                # Swap
                occ_count[_j] = _c1
                occ_value[_j] = _v1
                occ_count[_j + 1] = _c0
                occ_value[_j + 1] = _v0
        # Return
        return occ_value

    #endregion

    #region methods

    def _main(self):
        # Open tileset
        if cli.helper.ImgUtil.checkext(self.tileset):
            _tsetimg = cast(None|img.Img, cli.helper.ImgUtil.load(self.tileset))
            if _tsetimg is None: return 1
            _tileset = gb.GBTileUtil.from_img(_tsetimg)
        else:
            _tileset = cli.helper.GBUtil.tileset_load(self.tileset)
            if _tileset is None: return 1
        tileset:dict[gb.GBTile, int] = {}
        _i = 0
        for _tile in _tileset:
            if not (_tile in tileset):
                tileset[_tile] = _i
            _i += 1
        # Open input
        _input = cast(None|img.Img, cli.helper.ImgUtil.load(self.input))
        if _input is None: return 1
        # Make sure input is valid
        MAXSIZE = TILEDIM * TILESIZE
        if _input.width > MAXSIZE:
            print(f"Image width must be less than or equal to {MAXSIZE} pixels.", file = sys.stderr)
            return 1
        if _input.height > MAXSIZE:
            print(f"Image height must be less than or equal to {MAXSIZE} pixels.", file = sys.stderr)
            return 1
        # Create "tile data" from image
        input = gb.GBTileUtil.from_img(_input)
        input_w = _input.width // 8
        input_h = _input.height // 8
        print(f"Map Width:   {input_w} (${input_w:02X})")
        print(f"Map Height:  {input_h} (${input_h:02X})")
        # Create intermediate buffer
        buffer = data.DataBuffer(TILEDIM * input_h)
        _i = 0
        for _y in range(input_h):
            for _x in range(input_w):
                _tile = input[_i]
                _i += 1
                if _tile in tileset:
                    _value = min(0xFF, tileset[_tile])
                else:
                    _value = 0xFF
                buffer.write_byte(_value)
            for _x in range(input_w, TILEDIM):
                buffer.write_byte(0x00)
        # Determine values for end and RLE
        _occurances = self.__occurbyfreq(buffer)
        v_end = _occurances[0] # Least occurring value
        v_rle = _occurances[1] # Second least occurring value
        vspec = set([v_end, v_rle])
        # Create output
        output = data.DataBuffer()
        output.write_byte(v_end)
        output.write_byte(v_rle)
        _i = 0
        while _i < len(buffer):
            # Read byte
            _b = buffer[_i]
            _i += 1
            # Determine length
            _len = 1
            while _len < 255 and _i < len(buffer) and buffer[_i] == _b:
                _i += 1
                _len += 1
            # Write
            if _len != 1 or _b in vspec:
                output.write_byte(v_rle)
                output.write_byte(_b)
                output.write_byte(_len)
            else: output.write_byte(_b)
        output.write_byte(v_end)
        # Save output
        if not cli.helper.IOUtil.buffer_save(output, self.output):
            return 1
        # Success
        return 0

    #endregion

sys.exit(cmd_menu().execute(sys.argv))