__all__ = [\
    'LifePatternRule',]

import numpy as _np

from io import\
    StringIO as _StringIO

class LifePatternRule:
    """
    Represents a rule configuration for Conway's Game of Life
    """

    #region init

    def __init__(self,\
            b:tuple[int] = (3, ),\
            s:tuple[int] = (2, 3, )):
        """
        Initializer for LifePatternRule

        :param b:
            For dead cells, if the number of neighboring live cells is one these specified values, 
            then the cell can become alive; otherwise the cell remains dead.\n
            All specified values must be >= 0 and <= 8.
        :param s:
            For live cells, if the number of neighboring live cells is one these specified values, 
            then the cell can remain alive; otherwise the cell becomes dead.\n
            All specified values must be >= 0 and <= 8.
        :raise ValueError:
            One or more values in b are out of range\n
            or\n
            One or more values in s are out of range
        """
        ex = None
        # b
        try: self.__b = self.__tuple(b, "b")
        except ValueError as _ex: ex = _ex
        if ex is not None: raise ex
        # s
        try: self.__s = self.__tuple(s, "s")
        except ValueError as _ex: ex = _ex
        if ex is not None: raise ex

    #endregion

    #region operators

    def __repr__(self):
        return f"LifePatternRule({self.__b}, {self.__s})"
    
    def __str__(self):
        with _StringIO() as strio:
            # b
            strio.write('b')
            for v in self.__b:
                strio.write(str(v))
            # separator
            strio.write('/')
            # s
            strio.write('s')
            for v in self.__s:
                strio.write(str(v))
            # Return
            return strio.getvalue()

    def __eq__(self, other):
        return self.__equals(other)

    def __ne__(self, other):
        return not self.__equals(other)
    
    def __hash__(self):
        return hash(self.__b)

    #endregion

    #region properties

    @property
    def b(self):
        """
        For dead cells, if the number of neighboring live cells is one these specified values, 
        then the cell can become alive; otherwise the cell remains dead.
        """
        return self.__b
    
    @property
    def s(self):
        """
        For live cells, if the number of neighboring live cells is one these specified values, 
        then the cell can remain alive; otherwise the cell becomes dead.
        """
        return self.__s
        
    #endregion

    #region helper methods

    @classmethod
    def __tuple(cls, input:tuple[int], param:str):
        # Temp array
        temp = _np.empty(len(input), dtype = _np.uint8)
        for _i in range(len(input)):
            _value = input[_i]
            # Ensure value is valid
            if _value < 0 or _value > 8:
                raise ValueError(f"{param} contains one or more out of range values.")
            # Add to temp array
            temp[_i] = _value
        # Create tuple
        return tuple(_np.unique(temp))
    
    def __equals(self, other):
        if not isinstance(other, LifePatternRule):
            return False
        return self.__b == other.__b and self.__s == other.__s

    #endregion