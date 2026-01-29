import sys

import src.cli

class cmd_test(src.cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "This is a command description."

    #region required

    __string = src.cli.CLIRequiredDef(\
        name = "string",\
        desc = "String")
    __number = src.cli.CLIRequiredDef(\
        name = "number",\
        desc = "Number",\
        parse = src.cli.CLIParseUtil.to_int)

    #endregion

    #region optional

    __u8 = src.cli.CLIOptionWArgDef(\
        name = "u8",\
        short = 'B',\
        desc = "8-bit unsigned integer",\
        parse = src.cli.CLIParseUtil.to_uint8,\
        default = 0)
    __i8 = src.cli.CLIOptionWArgDef(\
        name = "i8",\
        short = 'b',\
        desc = "8-bit signed integer",\
        parse = src.cli.CLIParseUtil.to_int8,\
        default = 0)
    __u16 = src.cli.CLIOptionWArgDef(\
        name = "u16",\
        short = 'S',\
        desc = "16-bit unsigned integer",\
        parse = src.cli.CLIParseUtil.to_uint16,\
        default = 0)
    __i16 = src.cli.CLIOptionWArgDef(\
        name = "i16",\
        short = 's',\
        desc = "16-bit signed integer",\
        parse = src.cli.CLIParseUtil.to_int16,\
        default = 0)
    __u32 = src.cli.CLIOptionWArgDef(\
        name = "u32",\
        short = 'I',\
        desc = "32-bit unsigned integer",\
        parse = src.cli.CLIParseUtil.to_uint32,\
        default = 0)
    __i32 = src.cli.CLIOptionWArgDef(\
        name = "i32",\
        short = 'i',\
        desc = "32-bit signed integer",\
        parse = src.cli.CLIParseUtil.to_int32,\
        default = 0)
    __u64 = src.cli.CLIOptionWArgDef(\
        name = "u64",\
        short = 'L',\
        desc = "64-bit unsigned integer",\
        parse = src.cli.CLIParseUtil.to_uint64,\
        default = 0)
    __i64 = src.cli.CLIOptionWArgDef(\
        name = "i64",\
        short = 'l',\
        desc = "64-bit signed integer",\
        parse = src.cli.CLIParseUtil.to_int64,\
        default = 0)
    __f = src.cli.CLIOptionWArgDef(\
        name = "float",\
        short = 'f',\
        desc = "Floating-point decimal",\
        parse = src.cli.CLIParseUtil.to_float,\
        default = 0)

    #endregion

    #region methods

    def _main(self):
        print(f"string   {self.string}")
        print(f"number   {self.number}")
        print(f"u8       {self.u8}")
        print(f"i8       {self.i8}")
        print(f"u16      {self.u16}")
        print(f"i16      {self.i16}")
        print(f"u32      {self.u32}")
        print(f"i32      {self.i32}")
        print(f"u64      {self.u64}")
        print(f"i64      {self.i64}")
        print(f"float    {self.float}")
        return 0

    #endregion

if __name__ == '__main__':
    sys.exit(cmd_test().execute(sys.argv))