from sys import stderr

class IOUtil:
    """
    Utility for I/O-related operations
    """

    from data.DataBuffer import DataBuffer as __DataBuffer

    #region buffer

    @classmethod
    def buffer_load(cls, path:str):
        """
        Attempts to create a DataBuffer by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created DataBuffer (or None if load failed)
        """
        # Read bytes from file 
        try:
            with open(path, 'rb') as input:
                bytes = input.read()
        except Exception as e:
            print(f"ERROR: {e}", file = stderr)
            return None
        # Create buffer
        buffer = cls.__DataBuffer(len(bytes))
        for i in range(len(bytes)):
            buffer[i] = bytes[i]
        return buffer

    @classmethod
    def buffer_save(cls, buffer:__DataBuffer, path:str):
        """
        Attempts to save a DataBuffer to a file
        
        :param buffer:
            DataBuffer to save
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        try: 
            with open(path, 'wb') as output:
                output.write(bytes(buffer))
            return True
        except Exception as e:
            print(f"ERROR: {e}", file = stderr)
            return False

    #endregion

    #region str

    @classmethod
    def str_load(cls, path:str):
        """
        Attempts to create a string by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created string (or None if load failed)
        """
        try:
            with open(path, 'rt') as input:
                return input.read()
        except Exception as e:
            print(f"ERROR: {e}", file = stderr)
            return None

    @classmethod
    def str_save(cls, string:str, path:str):
        """
        Attempts to save a string to a file
        
        :param string:
            String to save
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        try: 
            with open(path, 'wt') as output:
                output.write(string)
            return True
        except Exception as e:
            print(f"ERROR: {e}", file = stderr)
            return False

    #endregion