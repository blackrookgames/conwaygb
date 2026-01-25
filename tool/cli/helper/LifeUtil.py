from numpy import uint64
from sys import stderr

class LifeUtil:
    """
    Utility for Life-related operations
    """

    from io import StringIO as __StringIO
    from cli.helper.IOUtil import IOUtil as __IOUtil
    from cli.helper.StringReader import StringReader as __StringReader
    from life.LifePattern import LifePattern as __LifePattern
    from life.LifePatternRule import LifePatternRule as __LifePatternRule

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
        string = cls.__IOUtil.str_load(path)
        if string is None: return None
        # Parse
        w = 0
        h = 0
        data = []
        _reader = cls.__StringReader(string)
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
                        print(_reader.error_unex_char(), file = stderr)
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
                print(_reader.error_unex_char(), file = stderr)
                return None
            # Add row
            if w < len(_row):
                w = len(_row)
            data.append(_row)
        # Create pattern
        pattern = cls.__LifePattern(width = w, height = h)
        for _y in range(len(data)):
            _row = data[_y]
            for _x in range(len(_row)):
                pattern[_x, _y] = _row[_x]
        # Success!!!
        return pattern

    @classmethod
    def pattern_save_txt(cls, pattern:__LifePattern, path:str):
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
        with cls.__StringIO() as strio:
            for y in range(pattern.height):
                for x in range(pattern.width):
                    strio.write('O' if pattern[x, y] else '.')
                strio.write('\n')
            return cls.__IOUtil.str_save(strio.getvalue(), path)

    #endregion