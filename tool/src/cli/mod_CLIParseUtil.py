__all__ = [\
    'CLIParseUtil',]

from sys import\
    stderr as _stderr

from ..helper.mod_ParseUtil import\
    ParseUtil as _ParseUtil
from ..helper.mod_ParseUtilStatus import\
    ParseUtilStatus as _ParseUtilStatus

class CLIParseUtil:
    """
    Utility for parsing command-line input
    """

    #region helper

    @classmethod
    def __parse_value(cls,\
            function,\
            typedesc:str,\
            input:str):
        result = function(input)
        if result.status == _ParseUtilStatus.PASS:
            return True, result.value
        print(f"{input} is not a valid {typedesc}.", file = _stderr)
        return False, None

    #endregion

    #region int

    @classmethod
    def to_int(cls,\
            input:str):
        """
        Attempts to parse input as an integer
        
        :param input: Input
        :return:
            Parse result
        """
        return cls.__parse_value(\
            _ParseUtil.to_int,\
            "integer",\
            input)
    
    @classmethod
    def to_uint8(cls,\
            input:str):
        """
        Attempts to parse input as an 8-bit unsigned integer
        
        :param input: Input
        :return:
            Parse result
        """
        return cls.__parse_value(\
            _ParseUtil.to_uint8,\
            "8-bit unsigned integer",\
            input)
    
    @classmethod
    def to_int8(cls,\
            input:str):
        """
        Attempts to parse input as an 8-bit signed integer
        
        :param input: Input
        :return:
            Parse result
        """
        return cls.__parse_value(\
            _ParseUtil.to_int8,\
            "8-bit signed integer",\
            input)
    
    @classmethod
    def to_uint16(cls,\
            input:str):
        """
        Attempts to parse input as a 16-bit unsigned integer
        
        :param input: Input
        :return:
            Parse result
        """
        return cls.__parse_value(\
            _ParseUtil.to_uint16,\
            "16-bit unsigned integer",\
            input)
    
    @classmethod
    def to_int16(cls,\
            input:str):
        """
        Attempts to parse input as a 16-bit signed integer
        
        :param input: Input
        :return:
            Parse result
        """
        return cls.__parse_value(\
            _ParseUtil.to_int16,\
            "16-bit signed integer",\
            input)
    
    @classmethod
    def to_uint32(cls,\
            input:str):
        """
        Attempts to parse input as a 32-bit unsigned integer
        
        :param input: Input
        :return:
            Parse result
        """
        return cls.__parse_value(\
            _ParseUtil.to_uint32,\
            "32-bit unsigned integer",\
            input)
    
    @classmethod
    def to_int32(cls,\
            input:str):
        """
        Attempts to parse input as a 32-bit signed integer
        
        :param input: Input
        :return:
            Parse result
        """
        return cls.__parse_value(\
            _ParseUtil.to_int32,\
            "32-bit signed integer",\
            input)
    
    @classmethod
    def to_uint64(cls,\
            input:str):
        """
        Attempts to parse input as a 64-bit unsigned integer
        
        :param input: Input
        :return:
            Parse result
        """
        return cls.__parse_value(\
            _ParseUtil.to_uint64,\
            "64-bit unsigned integer",\
            input)
    
    @classmethod
    def to_int64(cls,\
            input:str):
        """
        Attempts to parse input as a 64-bit signed integer
        
        :param input: Input
        :return:
            Parse result
        """
        return cls.__parse_value(\
            _ParseUtil.to_int64,\
            "64-bit signed integer",\
            input)

    #endregion

    #region float

    @classmethod
    def to_float(cls,\
            input:str):
        """
        Attempts to parse input as a floating-point decimal
        
        :param input: Input
        :return:
            Parse result
        """
        return cls.__parse_value(\
            _ParseUtil.to_float,\
            "floating-point decimal",\
            input)
    
    #endregion