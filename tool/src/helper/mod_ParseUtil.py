__all__ = [\
    'ParseUtil',\
    'U8_MIN',\
    'U8_MAX',\
    'I8_MIN',\
    'I8_MAX',\
    'U16_MIN',\
    'U16_MAX',\
    'I16_MIN',\
    'I16_MAX',\
    'U32_MIN',\
    'U32_MAX',\
    'I32_MIN',\
    'I32_MAX',\
    'U64_MIN',\
    'U64_MAX',\
    'I64_MIN',\
    'I64_MAX',]

from .mod_ParseUtilResult import\
    ParseUtilResult as _ParseUtilResult

U8_MIN = 0
U8_MAX = 0xFF
I8_MIN = -0x80
I8_MAX = 0x7F
U16_MIN = 0
U16_MAX = 0xFFFF
I16_MIN = -0x8000
I16_MAX = 0x7FFF
U32_MIN = 0
U32_MAX = 0xFFFFFFFF
I32_MIN = -0x80000000
I32_MAX = 0x7FFFFFFF
U64_MIN = 0
U64_MAX = 0xFFFFFFFFFFFFFFFF
I64_MIN = -0x8000000000000000
I64_MAX = 0x7FFFFFFFFFFFFFFF

class ParseUtil:
    """
    Utility for parsing input
    """

    #region int

    @classmethod
    def __int(cls,\
            input:str)\
            -> None|int:
        def _try(_input:str, _base:int = 10):
            try: return int(_input, base = _base)
            except: return None
        if len(input) == 0: return None
        match input[0]:
            case '0':
                if len(input) >= 2:
                    match input[1]:
                        case 'b': return _try(input[2:], _base = 2)
                        case 'B': return _try(input[2:], _base = 2)
                        case 'x': return _try(input[2:], _base = 16)
                        case 'X': return _try(input[2:], _base = 16)
                        case _: return _try(input)
                else: return _try(input)
            case '%': return _try(input[1:], _base = 2)
            case '$': return _try(input[1:], _base = 16)
        return _try(input)

    @classmethod
    def __to_int(cls,\
            input:str,\
            hard:None|tuple[int, int],\
            softmin:None|int,\
            softmax:None|int)\
            -> _ParseUtilResult[int]:
        """
        Assume\n
        if hard is not None, hard[0] < hard[1]
        """
        value = cls.__int(input)
        if value is None:
            return _ParseUtilResult[int].fail()
        # Hard check
        if hard is not None:
            if value < hard[0] or value > hard[1]:
                return _ParseUtilResult[int].fail()
        # Soft check
        if softmin is not None and value < softmin:
            return _ParseUtilResult[int].tolo()
        if softmax is not None and value > softmax:
            return _ParseUtilResult[int].tohi()
        # Success!!!
        return _ParseUtilResult[int].passs(value)
    
    @classmethod
    def to_int(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> _ParseUtilResult[int]:
        """
        Attempts to parse input as an integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parse result
        """
        return cls.__to_int(input, None, min, max)
    
    @classmethod
    def to_uint8(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> _ParseUtilResult[int]:
        """
        Attempts to parse input as an 8-bit unsigned integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parse result
        """
        return cls.__to_int(input, (U8_MIN, U8_MAX), min, max)
    
    @classmethod
    def to_int8(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> _ParseUtilResult[int]:
        """
        Attempts to parse input as an 8-bit signed integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parse result
        """
        return cls.__to_int(input, (I8_MIN, I8_MAX), min, max)
    
    @classmethod
    def to_uint16(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> _ParseUtilResult[int]:
        """
        Attempts to parse input as a 16-bit unsigned integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parse result
        """
        return cls.__to_int(input, (U16_MIN, U16_MAX), min, max)
    
    @classmethod
    def to_int16(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> _ParseUtilResult[int]:
        """
        Attempts to parse input as a 16-bit signed integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parse result
        """
        return cls.__to_int(input, (I16_MIN, I16_MAX), min, max)
    
    @classmethod
    def to_uint32(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> _ParseUtilResult[int]:
        """
        Attempts to parse input as a 32-bit unsigned integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parse result
        """
        return cls.__to_int(input, (U32_MIN, U32_MAX), min, max)
    
    @classmethod
    def to_int32(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> _ParseUtilResult[int]:
        """
        Attempts to parse input as a 32-bit signed integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parse result
        """
        return cls.__to_int(input, (I32_MIN, I32_MAX), min, max)
    
    @classmethod
    def to_uint64(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> _ParseUtilResult[int]:
        """
        Attempts to parse input as a 64-bit unsigned integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parse result
        """
        return cls.__to_int(input, (U64_MIN, U64_MAX), min, max)
    
    @classmethod
    def to_int64(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> _ParseUtilResult[int]:
        """
        Attempts to parse input as a 64-bit signed integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parse result
        """
        return cls.__to_int(input, (I64_MIN, I64_MAX), min, max)

    #endregion

    #region float

    @classmethod
    def to_float(cls,\
            input:str,\
            min:None|float,\
            max:None|float)\
            -> _ParseUtilResult[float]:
        """
        Attempts to parse input as a floating-point decimal
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parse result
        """
        try: value = float(input)
        except: return _ParseUtilResult[float].fail()
        # Range check
        if min is not None and value < min:
            return _ParseUtilResult[float].tolo()
        if max is not None and value > max:
            return _ParseUtilResult[float].tohi()
        # Success!!!
        return _ParseUtilResult[float].passs(value)
    
    #endregion