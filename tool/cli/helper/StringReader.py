class StringReader:
    """
    Represents a string reader
    """

    __FIRST = 1

    #region init

    def __init__(self, string:str):
        """
        Initializer for StringReader
        
        :param string:
            String to read
        """
        self.__string = string
        # Current position
        self.__pos = 0
        self.__row = self.__FIRST
        self.__col = self.__FIRST
        # Current character
        self.__updatechar()

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
    
    def error(self, message):
        """
        Creates an error message about the string

        :param message:
            Error message
        """
        return f"ERROR:\nLine {self.__row}, Column {self.__col}\n{message}"

    def error_unex_char(self):
        """
        Creates an error message about the current character being unexpected
        """
        return self.error(f"Unexpected character: {self.__chr}")

    #endregion