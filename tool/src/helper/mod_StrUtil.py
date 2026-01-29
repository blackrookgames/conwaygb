__all__ = [ 'StrUtil' ]

class StrUtil:
    """
    Utility for string-related operations
    """

    #region trimpnts

    @classmethod
    def trimpnts(cls, string:str):
        """
        Computes start and end points for trimming whitespace
        
        :param string:
            Input string
        :return:
            Start and end points for trimming whitespace\n
            If start and end points are equal, then the string contains only whitespace.
        """
        # Leading
        beg = 0
        while True:
            if beg == len(string):
                return 0, 0
            if string[beg] > ' ':
                break
            beg += 1
        # Trailing
        end = len(string)
        while string[end - 1] <= ' ':
            end -= 1
        # Return
        return beg, end

    #endregion