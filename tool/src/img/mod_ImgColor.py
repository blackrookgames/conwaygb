__all__ = [\
    'ImgColor',]

class ImgColor:
    """
    Represents a color
    """

    #region init

    def __init__(self,\
            r:int = 0,\
            g:int = 0,\
            b:int = 0,\
            a:int = 255):
        """
        Initializer for ImgColor
        
        :param r:
            Red value (0-255)
        :param g:
            Green value (0-255)
        :param b:
            Blue value (0-255)
        :param a:
            Alpha value (0-255)
        """
        self.__r = max(0, min(255, r))
        self.__g = max(0, min(255, g))
        self.__b = max(0, min(255, b))
        self.__a = max(0, min(255, a))

    #endregion

    #region operator
    
    def __repr__(self):
        return f"ImgColor(r = {self.__r}, g = {self.__g}, b = {self.__b}, a = {self.__a})"
    
    def __str__(self):
        return f"{self.__r}, {self.__g}, {self.__b}, {self.__a}"
    
    def __eq__(self, other):
        return self.__eq(other)
    
    def __ne__(self, other):
        return not self.__eq(other)

    def __hash__(self):
        return self.to_int()

    #endregion

    #region properties

    @property
    def r(self):
        """
        Red value (0-255)
        """
        return self.__r

    @property
    def g(self):
        """
        Green value (0-255)
        """
        return self.__g

    @property
    def b(self):
        """
        Blue value (0-255)
        """
        return self.__b
    
    @property
    def a(self):
        """
        Alpha value (0-255)
        """
        return self.__a

    #endregion

    #region helper methods

    def __eq(self, other):
        if not isinstance(other, ImgColor):
            return False
        return \
            self.__r == other.__r and \
            self.__g == other.__g and \
            self.__b == other.__b and \
            self.__a == other.__a

    #endregion

    #region methods

    def to_int(self) -> int:
        """
        Converts the color to an integer

        :return:
            Computed integer
        """
        return (self.__r << 24) | (self.__g << 16) | (self.__b << 8) | self.__a

    #endregion