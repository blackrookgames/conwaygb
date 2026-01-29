import numpy
import sys

from typing import cast

import src.cli as cli
import src.data as data
import src.img as img

TILESIZE = 8

class cmd_enbin(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Encode a binary file from data specified in a text file."

    #region required

    __input = cli.CLIRequiredDef(\
        name = "input",\
        desc = "Path to the input text file")
    __output = cli.CLIRequiredDef(\
        name = "output",\
        desc = "Path to the output binary file")

    #endregion

    #region helper methods

    @classmethod
    def __getdata(cls, binary:data.DataBuffer, string:str):
        pos = 0
        while pos < len(string):
            c = ord(string[pos])
            # whitespace
            if c <= 0x20:
                # Skip
                pos += 1
                continue
            # comment
            if c == 0x23:
                # Skip rest of line
                pos += 1
                while pos < len(string):
                    c = ord(string[pos])
                    pos += 1
                    if c == 0x0A or c == 0x0D:
                        break
                continue
            # possible value
            end = pos
            while True:
                end += 1
                if end >= len(string):
                    break
                if ord(string[end]) <= 0x20:
                    break
            potval = string[pos:end]
            if c == 0x2D: # This is a minus
                res, val = cli.CLIParseUtil.to_int8(potval)
            else:
                res, val = cli.CLIParseUtil.to_uint8(potval)
            if not res: return False
            binary.write_byte(val)
            pos = end
        return True

    #endregion

    #region methods

    def _main(self):
        # Open input
        input = cast(None|str, cli.helper.IOUtil.str_load(self.input))
        if input is None: return 1
        # Create binary
        binary = data.DataBuffer()
        if not self.__getdata(binary, input):
            return 1
        # Save
        if not cli.helper.IOUtil.buffer_save(binary, self.output):
            return 1
        # Success
        return 0

    #endregion

sys.exit(cmd_enbin().execute(sys.argv))