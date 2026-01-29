import numpy as np
import sys

from typing import cast

import src.cli as cli
import src.data as data
import src.img as img
import src.life as life

class cmd_sample(cli.CLICommand):

    TYPE_TXT = 'txt'
    TYPE_RLE = 'rle'
    TYPE_IMG = 'img'

    MAX_W = 40
    MAX_H = 36

    @property
    def _desc(self) -> None|str:
        return "Create a sample pattern"

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
        # Ensure pattern is valid
        if pattern.width > self.MAX_W:
            print(f"ERROR: Pattern width must be less than or equal to {self.MAX_W}.")
            return 1
        if pattern.height > self.MAX_H:
            print(f"ERROR: Pattern height must be less than or equal to {self.MAX_H}.")
            return 1
        # Sample
        sample = np.zeros((self.MAX_W, self.MAX_H), dtype = bool)
        _off_x = (self.MAX_W - pattern.width) // 2
        _off_y = (self.MAX_H - pattern.height) // 2
        for _y in range(pattern.height):
            for _x in range(pattern.width):
                sample[_off_x + _x, _off_y + _y] = pattern[_x, _y]
        # Output
        output = data.DataBuffer(size = (self.MAX_W * self.MAX_H) // 8)
        for _y in range(0, self.MAX_H, 2):
            for _x in range(0, self.MAX_W, 4):
                _byte = 0
                # First 2x2 block
                if sample[_x, _y]:
                    _byte |= 0b00000001
                if sample[_x + 1, _y]:
                    _byte |= 0b00000010
                if sample[_x, _y + 1]:
                    _byte |= 0b00000100
                if sample[_x + 1, _y + 1]:
                    _byte |= 0b00001000
                # Second 2x2 block
                if sample[_x + 2, _y]:
                    _byte |= 0b00010000
                if sample[_x + 3, _y]:
                    _byte |= 0b00100000
                if sample[_x + 2, _y + 1]:
                    _byte |= 0b01000000
                if sample[_x + 3, _y + 1]:
                    _byte |= 0b10000000
                # Write
                output.write_byte(_byte)
        if not cli.helper.IOUtil.buffer_save(output, self.output):
            return 1
        # Success
        return 0

    #endregion

sys.exit(cmd_sample().execute(sys.argv))