import numpy
import sys

from typing import cast

import src.cli as cli
import src.data as data
import src.img as img
import src.life as life

class cmd_life(cli.CLICommand):

    TYPE_TXT = 'txt'
    TYPE_RLE = 'rle'
    TYPE_IMG = 'img'

    @property
    def _desc(self) -> None|str:
        return "Convert a file containing life pattern data to a different format."

    #region required

    __input = cli.CLIRequiredDef(\
        name = "input",\
        desc = "Path to the input file")
    __output = cli.CLIRequiredDef(\
        name = "output",\
        desc = "Path to the output file")

    #endregion

    #region optional

    __itype = cli.CLIOptionWArgDef(\
        name = "itype",\
        short = 'i',\
        desc = f"Input type. Allowed values: {TYPE_TXT}, {TYPE_RLE}, {TYPE_IMG}")
    __otype = cli.CLIOptionWArgDef(\
        name = "otype",\
        short = 'o',\
        desc = f"Output type. Allowed values: {TYPE_TXT}, {TYPE_RLE}, {TYPE_IMG}")

    #endregion

    #region helper methods

    @classmethod
    def __gettype(cls, option:None|str, path:str):
        # Is type undefined?
        if option is None:
            # Parse as image?
            if cli.helper.ImgUtil.checkext(path):
                return cls.TYPE_IMG
            # Parse as RLE?
            if path.endswith(".rle"):
                return cls.TYPE_RLE
            # Parse as text
            return cls.TYPE_TXT
        # No, validate the type
        match option:
            case cls.TYPE_TXT: return cls.TYPE_TXT
            case cls.TYPE_RLE: return cls.TYPE_RLE
            case cls.TYPE_IMG: return cls.TYPE_IMG
        print(f"ERROR: Unknown type: {option}", file = sys.stderr)
        return None

    #endregion

    #region methods

    def _main(self):
        # Determine input type
        itype = self.__gettype(self.itype, self.input)
        if itype is None: return 1
        # Determine output type
        otype = self.__gettype(self.otype, self.output)
        if otype is None: return 1
        # Input
        match itype:
            case self.TYPE_TXT:
                pattern = cli.helper.LifeUtil.pattern_load_txt(self.input)
                if pattern is None: return 1
            case self.TYPE_RLE:
                pattern = cli.helper.LifeUtil.pattern_load_rle(self.input)
                if pattern is None: return 1
            case self.TYPE_IMG:
                _img = cast(None | img.Img, cli.helper.ImgUtil.load(self.input))
                if _img is None: return 1
                pattern = life.LifePatternUtil.from_img(_img)
            case _: return 1 # Should never happen
        # Output
        match otype:
            case self.TYPE_TXT:
                if not cli.helper.LifeUtil.pattern_save_txt(pattern, self.output):
                    return 1
            case self.TYPE_RLE:
                if not cli.helper.LifeUtil.pattern_save_rle(pattern, self.output):
                    return 1
            case self.TYPE_IMG:
                _img = life.LifePatternUtil.to_img(pattern)
                if not cli.helper.ImgUtil.save(_img, self.output):
                    return 1
            case _: return 1 # Should never happen
        # Success
        return 0

    #endregion

sys.exit(cmd_life().execute(sys.argv))