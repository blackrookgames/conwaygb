__all__ = [ 'ErrorUtil' ]

class ErrorUtil:
    """
    Utility for errors and error checking
    """

    #region valid_int

    def valid_int(value, param:None|str = None):
        """
        Validates an input value as an integer

        :param param:
            Parameter name (assuming value is an argument for a function)
        :return:
            Value as an integer
        :raises TypeValue:
            value is not a valid integer
        """
        try:
            return int(value)
        except:
            if param is not None:
                raise TypeError(f"{param} is not a valid integer.")
            else:
                raise TypeError(f"{value} is not a valid integer.")

    #endregion

    #region valid_float

    def valid_float(value, param:None|str = None):
        """
        Validates an input value as a floating-point number

        :param param:
            Parameter name (assuming value is an argument for a function)
        :return:
            Value as an floating-point number
        :raises TypeValue:
            value is not a valid floating-point number
        """
        try:
            return float(value)
        except:
            if param is not None:
                raise TypeError(f"{param} is not a valid floating-point number.")
            else:
                raise TypeError(f"{value} is not a valid floating-point number.")

    #endregion

    #region valid_bool

    def valid_bool(value, param:None|str = None):
        """
        Validates an input value as a boolean value

        :param param:
            Parameter name (assuming value is an argument for a function)
        :return:
            Value as a boolean value
        :raises TypeValue:
            value is not a valid boolean value
        """
        try:
            return bool(value)
        except:
            if param is not None:
                raise TypeError(f"{param} is not a valid boolean value.")
            else:
                raise TypeError(f"{value} is not a valid boolean value.")

    #endregion

    #region valid_str

    def valid_str(value, param:None|str = None):
        """
        Validates an input value as a string

        :param param:
            Parameter name (assuming value is an argument for a function)
        :return:
            Value as an string
        :raises TypeValue:
            value is not a valid string
        """
        try:
            return str(value)
        except:
            if param is not None:
                raise TypeError(f"{param} is not a valid string.")
            else:
                raise TypeError(f"{value} is not a valid string.")

    #endregion