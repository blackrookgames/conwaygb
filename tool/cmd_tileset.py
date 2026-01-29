import numpy
import sys

from typing import cast

import src.cli as cli
import src.gb as gb
import src.data as data
import src.img as img

TILESIZE = 8

class cmd_tileset(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Creates a tileset from an image."

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
        # Create output
        output = gb.GBTileUtil.from_img(input)
        if not cli.helper.GBUtil.tileset_save(output, self.outbin):
            return 1
        # Success
        return 0

    #endregion

sys.exit(cmd_tileset().execute(sys.argv))