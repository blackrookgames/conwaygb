__all__ = [\
    'LifeUtil',]

from io import\
    StringIO as _StringIO
from sys import\
    stderr as _stderr

from ..mod_CLIParseUtil import\
    CLIParseUtil as _CLIParseUtil
from .mod_IOUtil import\
    IOUtil as _IOUtil
from .mod_StringReader\
    import StringReader as _StringReader
from ...helper.mod_StrUtil import\
    StrUtil as _StrUtil
from ...life.mod_LifePattern import\
    LifePattern as _LifePattern
from ...life.mod_LifePatternRule import\
    LifePatternRule as _LifePatternRule

class LifeUtil:
    """
    Utility for Life-related operations
    """

    #region pattern txt

    @classmethod
    def pattern_load_txt(cls, path:str):
        """
        Attrmpts to create a pattern using data from a text file
        
        :param path:
            Path of input file
        :return:
            Created life pattern
        """
        def _iscomment(_chr):
            return _chr == '#' or _chr == '!'
        # Load string
        string = _IOUtil.str_load(path)
        if string is None: return None
        # Parse
        w = 0
        h = 0
        data = []
        _reader = _StringReader(string)
        while not _reader.eof:
            # Find non-whitespace
            _reader.skip_white()
            if _reader.eof: break
            # Is this a comment?
            if _iscomment(_reader.chr):
                _reader.skip_line()
                continue
            # Parse line
            h += 1
            _row = []
            while not _reader.eol:
                # Is this whitespace?
                if _reader.white:
                    break
                # Is this a comment?
                if _iscomment(_reader.chr):
                    _reader.skip_eol()
                    break
                # Parse
                match _reader.chr:
                    case '.': _row.append(False)
                    case 'O': _row.append(True)
                    case '*': _row.append(True)
                    case _:
                        print(_reader.error_unex_char(), file = _stderr)
                        return None
                _reader.next()
            # Ensure rest of line contains only whitespace of comments
            while not _reader.eol:
                if _reader.white:
                    _reader.next()
                    continue
                if _iscomment(_reader.chr):
                    _reader.skip_eol()
                    break
                print(_reader.error_unex_char(), file = _stderr)
                return None
            # Add row
            if w < len(_row):
                w = len(_row)
            data.append(_row)
        # Create pattern
        pattern = _LifePattern(width = w, height = h)
        for _y in range(len(data)):
            _row = data[_y]
            for _x in range(len(_row)):
                pattern[_x, _y] = _row[_x]
        # Success!!!
        return pattern

    @classmethod
    def pattern_save_txt(cls, pattern:_LifePattern, path:str):
        """
        Attrmpts to save pattern data to a text file\n
        Note that any rule configurations will be lost
        
        :param pattern:
            Life pattern
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        with _StringIO() as strio:
            for y in range(pattern.height):
                for x in range(pattern.width):
                    strio.write('O' if pattern[x, y] else '.')
                strio.write('\n')
            return _IOUtil.str_save(strio.getvalue(), path)

    #endregion

    #region pattern rle

    @classmethod
    def pattern_load_rle(cls, path:str):
        """
        Attrmpts to create a pattern using data from an RLE file
        
        :param path:
            Path of input file
        :return:
            Created life pattern
        """
        def _parsehdrdef(\
                _hdrdefs:dict[str, str],\
                _reader:_StringReader,\
                _stop:int):
            # Leading whitespace; this also checks if there is only whitespace
            while True:
                if _reader.pos >= _stop:
                    return True
                if not _reader.white:
                    break
                _reader.next()
            #region Parse name
            _name_beg = _reader.pos
            while True:
                if _reader.pos >= _stop:
                    print(_reader.error("Equals sign expected"), file = _stderr)
                    return False
                if _reader.white or _reader.chr == '=':
                    name = _reader.string[_name_beg:_reader.pos]
                    break
                _reader.next()
            # Name sure name is specified
            if name == '':
                print(_reader.error("Name must precede equals sign"), file = _stderr)
                return False
            # Skip over whitespace and equals sign
            while True:
                if _reader.pos >= _stop:
                    print(_reader.error("Equals sign expected"), file = _stderr)
                    return False
                if _reader.chr == '=':
                    _reader.next()
                    break
                if not _reader.white:
                    print(_reader.error_unex_char(), file = _stderr)
                    return False
                _reader.next()
            #endregion
            # Parse value
            while _reader.pos < _stop:
                if not _reader.white:
                    break
                _reader.next()
            _value_beg = _reader.pos
            while _reader.pos < _stop:
                if _reader.white:
                    break
                _reader.next()
            value = _reader.string[_value_beg:_reader.pos]
            # Trailing whitespace
            while _reader.pos < _stop:
                if not _reader.white:
                    print(_reader.error_unex_char(), file = _stderr)
                    return False
                _reader.next()
            # Add definition
            _hdrdefs[name.lower()] = value
            # Success!!!
            return True
        def _parsexy(_value:str, _name:str):
            _r, _v = _CLIParseUtil.to_int(_value)
            if not _r:
                return False, 0
            if _v < 0:
                print(f"ERROR: {_name} cannot be negative", file = _stderr)
                return False, 0
            return True, _v
        def _parserule(_value:str, _name:str):
            def __invalid(__value):
                print(f"{__value} is not a valid pattern rule.", file = _stderr)
                return False, _LifePatternRule()
            if len(_value) == 0:
                return __invalid(_value)
            # b
            _char = _value[0]
            if _char == 'B' or _char == 'b':
                _i = 1
            elif _char >= '0' and _char <= '9':
                _i = 0
            else:
                return __invalid(_value)
            _b = []
            while True:
                if _i == len(_value):
                    return __invalid(_value)
                _char = _value[_i]
                _i += 1
                if _char == '/':
                    break
                if _char < '0' or _char > '8':
                    return __invalid(_value)
                _b.append(int(_char))
            if len(_b) == 0:
                return __invalid(_value)
            # s
            _char = _value[_i]
            if _char == 'S' or _char == 's':
                _i += 1
            elif _char < '0' or _char > '9':
                return __invalid(_value)
            _s = []
            while _i < len(_value):
                _char = _value[_i]
                _i += 1
                if _char < '0' or _char > '8':
                    return __invalid(_value)
                _s.append(int(_char))
            if len(_s) == 0:
                return __invalid(_value)
            # Success!!!
            return True, _LifePatternRule(b = tuple(_b), s = tuple(_s))
        def _parsedata(\
                _pattern:_LifePattern,\
                _reader:_StringReader):
            def __inc(\
                    __reader:_StringReader,\
                    __i:int,\
                    __size:int,\
                    __count:int):
                __i += __count
                if __i > __size:
                    print(__reader.error("Exceeded cell count"), file = _stderr)
                    return -1
                return __i
            def __writecell(
                    __pattern:_LifePattern,\
                    __i:int,\
                    __value:bool,\
                    __reader:_StringReader,\
                    __size:int):
                # Increment first
                __j = __inc(__reader, __i, __size, 1)
                if __j == -1: return -1
                # Then set value
                __pattern[__i % __pattern.width, __i // __pattern.width] = __value
                return __j
            def __cellvalue(__chr):
                if __chr == 'O' or __chr == 'o':
                    return 1
                if __chr == 'B' or __chr == 'b':
                    return 0
                return -1
            def __nextrow(
                    __pattern:_LifePattern,\
                    __i:int,\
                    __count:int,\
                    __reader:_StringReader,\
                    __size:int):
                # Get X-coordinate
                __x = __i % __pattern.width
                # If at end of line, ignore 1 of them
                if __i > 0 and __x == 0:
                    __count -= 1
                # Next line
                if __count == 0:
                    return __i
                return __inc(__reader, __i, __size, __pattern.width * __count - __x)
            _size = _pattern.width * _pattern.height
            _i = 0
            if _size > 0:
                while True:
                    # End of file (FAIL)?
                    if _reader.eof:
                        print(_reader.error_unex_end(), file = _stderr)
                        return False
                    # Comment?
                    elif _reader.chr == '#':
                        _reader.skip_line()
                        continue
                    # Whitespace?
                    elif _reader.white:
                        pass
                    # End of data?
                    elif _reader.chr == '!':
                        break
                    # End of line?
                    elif _reader.chr == '$':
                        # Find following
                        _count = 1
                        while True:
                            _chr = _reader.peek()
                            if _chr == '':
                                print(_reader.error_unex_end(), file = _stderr)
                                return False
                            if _chr == '$':
                                _count += 1
                            elif _chr > ' ':
                                break
                            _reader.next()
                        # Next rows
                        _i = __nextrow(_pattern, _i, _count, _reader, _size)
                        if _i == -1: return False
                    # Cell values (or multiple new rows)?
                    else:
                        # One cell?
                        _cellvalue = __cellvalue(_reader.chr)
                        if _cellvalue != -1:
                            _i = __writecell(_pattern, _i, _cellvalue == 1, _reader, _size)
                            if _i == -1: return False
                        # Multiple?
                        elif _reader.chr >= '0' and _reader.chr <= '9':
                            _count = int(_reader.chr)
                            # Extract rest of number
                            _reader.next()
                            while True:
                                if _reader.eof:
                                    print(_reader.error_unex_end(), file = _stderr)
                                    return False
                                if _reader.chr < '0' or _reader.chr > '9':
                                    break
                                _count *= 10
                                _count += int(_reader.chr)
                                _reader.next()
                            # Cell?
                            _reader.skip_white()
                            _cellvalue = __cellvalue(_reader.chr)
                            if _cellvalue != -1:
                                while _count > 0:
                                    _i = __writecell(_pattern, _i, _cellvalue == 1, _reader, _size)
                                    if _i == -1: return False
                                    _count -= 1
                            # New rows?
                            elif _reader.chr == '$':
                                _i = __nextrow(_pattern, _i, _count, _reader, _size)
                                if _i == -1: return False
                            # Unexpected (FAIL)?
                            else:
                                print(_reader.error_unex_char(), file = _stderr)
                                return False
                        # Unexpected (FAIL)?
                        else:
                            print(_reader.error_unex_char(), file = _stderr)
                            return False
                    # Next
                    _reader.next()
            else:
                if _reader.chr != '!':
                    print(_reader.error("Exceeded cell count"), file = _stderr)
                    return False
            # Success!!!
            return True
        # Load string
        string = _IOUtil.str_load(path)
        if string is None: return None
        # Begin parsing
        reader = _StringReader(string)
        # Find header
        while True:
            # End of file?
            if reader.eof:
                print(reader.error_unex_end(), file = _stderr)
                return None
            # Whitespace?
            if reader.white:
                reader.next()
                continue
            # Comment?
            if reader.chr == '#':
                reader.skip_line()
                continue
            # Header found!
            break
        # Parse header
        _hdrreader = _StringReader(reader)
        hdrdefs:dict[str, str] = {}
        while True:
            # End of line?
            if reader.eol:
                if not _parsehdrdef(hdrdefs, _hdrreader, reader.pos):
                    return None
                break
            # Comment?
            if reader.chr == '#':
                if not _parsehdrdef(hdrdefs, _hdrreader, reader.pos):
                    return None
                reader.skip_eol()
                break
            # Comma?
            if reader.chr == ',':
                if not _parsehdrdef(hdrdefs, _hdrreader, reader.pos):
                    return None
                _hdrreader.next()
                reader.next()
                continue
            # Next
            reader.next()
        reader.next()
        # Look thru defs
        hdr_x = None
        hdr_y = None
        hdr_rule = None
        for _n, _v in hdrdefs.items():
            match _n:
                case 'x':
                    _r, hdr_x = _parsexy(_v, _n)
                    if not _r: return None
                case 'y':
                    _r, hdr_y = _parsexy(_v, _n)
                    if not _r: return None
                case 'rule':
                    _r, hdr_rule = _parserule(_v, _n)
                    if not _r: return None
                case _:
                    print(f"WARNING: Unknown parameter: {_n}")
        if hdr_x is None:
            print("ERROR: Required parameter x has not been defined.")
            return None
        if hdr_y is None:
            print("ERROR: Required parameter y has not been defined.")
            return None
        if hdr_rule is None:
            hdrdefs = _LifePatternRule()
        # Init pattern
        pattern = _LifePattern(\
            width = hdr_x,\
            height = hdr_y,\
            rule = hdr_rule)
        # Parse data
        if not _parsedata(pattern, reader):
            return None
        # Success!!!
        return pattern

    @classmethod
    def pattern_save_rle(cls, pattern:_LifePattern, path:str):
        """
        Attempts to save pattern data to an RLE file
        
        :param pattern:
            Life pattern
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        def _writevalue(
                _strio:_StringIO,\
                _value:bool,\
                _count:int):
            if _count == 0: return
            if _count > 1: _strio.write(str(_count))
            _strio.write('o' if _value else 'b')
        with _StringIO() as strio:
            # Header
            strio.write(f"x = {pattern.width}, y = {pattern.height}, rule = {pattern.rule}\n")
            # Data
            for y in range(pattern.height):
                value = False
                count = 0
                for x in range(pattern.width):
                    if pattern[x, y] == value:
                        count += 1
                    else:
                        _writevalue(strio, value, count)
                        value = not value
                        count = 1
                _writevalue(strio, value, count)
                if (y + 1) < pattern.height:
                    strio.write("$")
            strio.write("!\n")
            # Save
            return _IOUtil.str_save(strio.getvalue(), path)

    #endregion