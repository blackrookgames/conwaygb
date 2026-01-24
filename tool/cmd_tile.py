import numpy
import sys

from typing import cast

import cli._00 as cli
import data._00 as data
import img._00 as img

TILESIZE = 8

class cmd_tile(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Creates tile data from an image."

    #region required

    __input = cli.CLIRequiredDef(\
        name = "input",\
        desc = "Path to the input file")
    __outbin = cli.CLIRequiredDef(\
        name = "outbin",\
        desc = "Path to the output *.bin file")

    #endregion

    #region methods

    def _main(self):
        # Open input
        input = cast(None|img.Img, cli.helper.ImgUtil.load(self.input))
        if input is None: return 1
        # Determine number of tiles
        tcount_col = input.width // TILESIZE
        tcount_row = input.height // TILESIZE
        tcount = tcount_col * tcount_row
        # Extract tile data
        tiles = numpy.empty((tcount, TILESIZE, TILESIZE), dtype=numpy.ubyte)
        for _i in range(tcount):
            _off_x = (_i % tcount_col) * TILESIZE
            _off_y = (_i // tcount_col) * TILESIZE
            for _y in range(TILESIZE):
                for _x in range(TILESIZE):
                    _pixel = input[_off_x + _x, _off_y + _y]
                    _value = ((_pixel.r + _pixel.g + _pixel.b) / 3) / 255
                    tiles[_i, _x, _y] = round(_value * 3) ^ 0b11
        # Create output
        output = data.DataBuffer(size = tcount * TILESIZE * 2)
        for _i in range(tcount):
            for _y in range(TILESIZE):
                _b0 = 0
                _b1 = 0
                _m = 0b10000000
                for _x in range(TILESIZE):
                    _pixel = tiles[_i, _x, _y]
                    if (_pixel & 0b01) != 0: _b0 |= _m
                    if (_pixel & 0b10) != 0: _b1 |= _m
                    _m >>= 1
                output.write_byte(_b0)
                output.write_byte(_b1)
        if not cli.helper.IOUtil.buffer_save(output, self.outbin):
            return 1
        # Success
        return 0

    #endregion

sys.exit(cmd_tile().execute(sys.argv))