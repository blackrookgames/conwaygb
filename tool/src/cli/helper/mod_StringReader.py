__all__ = [\
    'StringReader',]

from io import\
    StringIO as _StringIO

class StringReader:
    """
    Represents a string reader
    """

    __FIRST = 1

    #region init

    def __init__(self, src):
        """
        Initializer for StringReader
        
        :param src:
            Source to read\n
            If str, then this will be the string that will be read\n
            If StringReader, then the state of the source reader will be duplicated to the 
                current StringReader. This can be useful for "peeking".
        :raise TypeError:
            src type if not supported
        """
        if isinstance(src, str):
            self.__string = src
            # Current position
            self.__pos = 0
            self.__row = self.__FIRST
            self.__col = self.__FIRST
            # Current character
            self.__updatechar()
        elif isinstance(src, StringReader):
            self.__string = src.__string
            # Current position
            self.__pos = src.__pos
            self.__row = src.__row
            self.__col = src.__col
            # Current character
            self.__chr = src.__chr
            self.__white = src.__white
            self.__eof = src.__eof
            self.__eol = src.__eol
        else:
            raise TypeError(f"{type(src)} is not supported.")


    #endregion

    #region properties

    @property
    def string(self):
        """
        String that the reader is reading
        """
        return self.__string

    @property
    def pos(self):
        """
        Position of the reader; 0 is the first position
        """
        return self.__pos

    @property
    def row(self):
        """
        Row of the reader; 1 is the first row
        """
        return self.__row

    @property
    def col(self):
        """
        Column of the reader; 1 is the first column
        """
        return self.__col

    @property
    def chr(self):
        """
        Character at the current position of the reader
        """
        return self.__chr

    @property
    def white(self):
        """
        Whether or not the character at the current position of the reader is whitespace
        """
        return self.__white

    @property
    def eof(self):
        """
        Whether or not the reader has reached the end of the string
        """
        return self.__eof

    @property
    def eol(self):
        """
        Whether or not the reader has reached the end of the current line in the string
        """
        return self.__eol

    #endregion

    #region helper methods
    
    def __updatechar(self):
        if self.__pos < len(self.__string):
            self.__chr = self.__string[self.__pos]
            self.__white = self.__chr <= ' '
            self.__eof = False
            self.__eol = self.__chr == '\n'
        else:
            self.__chr = '\0'
            self.__white = True
            self.__eof = True
            self.__eol = True

    #endregion

    #region methods

    def next(self):
        """
        Advances to the next character in the string.\n
        If the end of the string has already been reached, nothing happens. 
        """
        if self.__eof: return
        # Update position
        self.__pos += 1
        if self.__eol:
            self.__row += 1
            self.__col = self.__FIRST
        else:
            self.__col += 1
        # Update character
        self.__updatechar()
    
    def peek(self):
        """
        Takes a peek at the next character in the string

        :return:
            Next character in string (or '' if EOF)
        """
        if self.__eof: return ''
        return self.__string[self.__pos + 1]
    
    def read_line(self):
        """
        Reads to the end of the current line

        :return:
            Read content
        """
        with _StringIO() as strio:
            while not self.__eol:
                strio.write(self.__chr)
                self.next()
            return strio.getvalue()

    def skip(self, count:int):
        """
        Skips the specified number of characters

        :param count:
            Number of characters to skip
        :return:
            Number of characters skipped (may be less than count if eof is reached)
        :raise ValueError:
            count is negative
        """
        if count < 0:
            raise ValueError("count cannot be negative.")
        skipped = 0
        while (not self.__eof) and skipped < count:
            skipped += 1
            self.next()
        return skipped
    
    def skip_eol(self):
        """
        Skips to the end of the current line
        """
        while not self.__eol:
            self.next()
    
    def skip_line(self):
        """
        Skips to the next line
        """
        self.skip_eol()
        if not self.__eof:
            self.next()
    
    def skip_white(self):
        """
        Skips to next non-whitespace character\n
        If current character is not whitespace, nothing happens.
        """
        while (not self.__eof) and self.__white:
            self.next()
    
    def error(self, message, lineonly = False):
        """
        Creates an error message about the string

        :param message:
            Error message
        :param lineonly:
            If true, then the column will not be added
        """
        with _StringIO() as strio:
            # ERROR
            strio.write("ERROR: ")
            # Line
            strio.write(f"Line: {self.__row} ")
            # Column
            if not lineonly:
                strio.write(f"Column: {self.__col} ")
            # Message
            strio.write(message)
            # Return
            return strio.getvalue()

    def error_unex_char(self):
        """
        Creates an error message about the current character being unexpected
        """
        return self.error(f"Unexpected character: {self.__chr}")

    def error_unex_end(self):
        """
        Creates an error message indicating an unexpected end of file\n
        Note that the actual state of the reader is not checked and will not be modified.
        """
        return self.error(f"Unexpected end of file.", lineonly = True)

    #endregion