import numpy
import sys

from typing import cast

import src.cli as cli
import src.gb as gb
import src.data as data
import src.img as img

TILESIZE = 8

class cmd_tilemap(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Creates a tilemap from an image."

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
        input = gb.GBTileUtil.from_img(_input)
        input_w = _input.width // 8
        input_h = _input.height // 8
        print(f"Map Width:   {input_w} (${input_w:02X})")
        print(f"Map Height:  {input_h} (${input_h:02X})")
        print(f"Total Size:  {len(input)} (${len(input):04X})")
        # Create output
        output = data.DataBuffer(len(input))
        for _tile in input:
            if _tile in tileset:
                _value = min(0xFF, tileset[_tile])
            else:
                _value = 0xFF
            output.write_byte(_value)
        # Save output
        if not cli.helper.IOUtil.buffer_save(output, self.output):
            return 1
        # Success
        return 0

    #endregion

sys.exit(cmd_tilemap().execute(sys.argv))