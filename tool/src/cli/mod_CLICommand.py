__all__ = [\
    'CLICommand',]

import shutil as _shutil

from sys import\
    stderr as _stderr
from typing import\
    cast as _cast

from .mod_CLIParamCollection import\
    CLIParamCollection as _CLIParamCollection
from .mod_CLIOptionFlag import\
    CLIOptionFlag as _CLIOptionFlag
from .mod_CLIOptionFlagDef import\
    CLIOptionFlagDef as _CLIOptionFlagDef
from .mod_CLIOptionWArg import\
    CLIOptionWArg as _CLIOptionWArg
from .mod_CLIOptionWArgDef import\
    CLIOptionWArgDef as _CLIOptionWArgDef
from .mod_CLIRequired import\
    CLIRequired as _CLIRequired
from .mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

class CLICommand:
    """
    Represents a command
    """

    #region init
    
    def __init__(self):
        """
        Initializer for CLICommand
        """
        def _recursive(_items:_CLIParamCollection, _type):
            # Check bases first
            for _base in _type.__bases__:
                _recursive(_items, _base)
            # Now check this
            for _varname, _value in _type.__dict__.items():
                # Is it a required parameter?
                if isinstance(_value, _CLIRequiredDef):
                    _items.add_reqparam(_CLIRequired(_varname, _value))
                # Is it an optional flag parameter?
                if isinstance(_value, _CLIOptionFlagDef):
                    _items.add_optparam(_CLIOptionFlag(_varname, _value))
                # Is it an optional parameter with an argument?
                if isinstance(_value, _CLIOptionWArgDef):
                    _items.add_optparam(_CLIOptionWArg(_varname, _value))
            # Finish
            return
        self.__params:_CLIParamCollection = _CLIParamCollection()
        _recursive(self.__params, type(self))

    #endregion

    #region helper properties

    @property
    def _help(self) -> None|str:
        return "help"
    
    @property
    def _desc(self) -> None|str:
        return None

    #endregion

    #region helper methods
    
    def __help(self, cmdname:None|str):
        #region Command-line
        # name
        if cmdname is None:
            print("cmd", end = "")
        else:
            print(cmdname, end = "")
        # help
        if self._help is not None:
            print(f" [--{self._help}]", end = "")
        # optional
        for _param in self.__params.optparams:
            if isinstance(_param, _CLIOptionWArg):
                print(f" [--{_param.name} <value>]", end = "")
            else:
                print(f" [--{_param.name}]", end = "")
        # required
        for _param in self.__params.reqparams:
            print(f" <{_param.name}>", end = "")
        # end
        print()
        #endregion
        #region Description
        if self._desc is not None:
            print()
            print(self._desc)
        #endregion
        #region Parameters and Flags
        TERMLEFT = 2
        TERMHELP = "Displays help information"
        termwidth = _shutil.get_terminal_size().columns
        namewidth = 0
        shortwidth = 0
        def _print_col(_name:str, _short:None|str, _desc:None|str,\
                _namewidth:int, _shortwidth:int, _descwidth:int):
            _indent = TERMLEFT + _namewidth + _shortwidth
            # First line
            print(f"{(' ' * TERMLEFT)}{_name.ljust(_namewidth)}", end = "")
            if _short is not None:
                print((f"-{_short}").ljust(_shortwidth), end = "")
            else:
                print((' ' * _shortwidth), end = "")
            if _desc is not None:
                _end = len(_desc) < _descwidth
                print(_desc[0:(len(_desc) if _end else _descwidth)])
            else:
                _end = True
                print()
            # Following lines
            _start = _descwidth
            while not _end:
                _stop = _start + _descwidth
                _end = _stop >= len(_desc)
                if _end: _stop = len(_desc)
                print(f"{(' ' * _indent)}{_desc[_start:_stop]}")
                _start += _descwidth
        def _print_nocol(_name:str, _short:None|str, _desc:None|str):
            print()
            print(_name)
            if _short is not None:
                print(f"-{_short}")
            if _desc is not None:
                print(_desc)
        for _param in self.__params.reqparams:
            if namewidth < len(_param.name):
                namewidth = len(_param.name)
        for _param in self.__params.optparams:
            _len = 2 + len(_param.name)
            if namewidth < _len:
                namewidth = _len
            _len = 1 + len(_param.short)
            if shortwidth < _len:
                shortwidth = _len
        if self._help is not None:
            _len = 2 + len(self._help)
            if namewidth < _len:
                namewidth = _len
        namewidth += 3
        shortwidth += 3
        descwidth = termwidth - TERMLEFT - namewidth - shortwidth
        if descwidth > 0:
            # Print with columns
            print()
            for _param in self.__params.reqparams:
                _print_col(_param.name, None, _param.desc,\
                    namewidth, shortwidth, descwidth)
            if self._help is not None:
                _print_col(f"--{self._help}", None, TERMHELP,\
                    namewidth, shortwidth, descwidth)
            for _param in self.__params.optparams:
                _print_col(f"--{_param.name}", _param.short, _param.desc,\
                    namewidth, shortwidth, descwidth)
        else:
            # Print without columns
            for _param in self.__params.reqparams:
                _print_nocol(_param.name, None, _param.desc)
            if self._help is not None:
                _print_nocol(f"--{self._help}", None, TERMHELP)
            for _param in self.__params.optparams:
                _print_nocol(f"--{_param.name}", _param.short, _param.desc)
        #endregion
        # Success!!!
        print()
        return 0

    #endregion
    
    #region methods
        
    def execute(self,\
            argv:list[str])\
            -> int:
        """
        Executes the command
        
        :param args:
            Command-line arguments (including the name)
        :return:
            Exit code
        """
        if len(argv) == 0: return self.__help(None)
        if len(argv) == 1: return self.__help(argv[0])
        # Define default values for options
        for _param in self.__params.optparams:
            setattr(self, _param.name, _param.default)
        # Gather arguments
        reqargs:list[str] = []
        optargs:list[str|tuple[str, str]] = []
        _help = self._help
        if _help is not None: _help = "--" + _help
        _optend = False
        _optin = None
        for _i in range(1, len(argv)):
            _input = argv[_i]
            # Was the last input declaring an optional parameter?
            if _optin is not None:
                optargs.append((_optin, _input))
                _optin = None
                continue
            # Could this be optional input?
            if (not _optend) and _input.startswith('-'):
                # Is this a call for help?
                if _help is not None and _input == _help:
                    return self.__help(argv[0])
                # No! Is it the name of an option?
                if _input.startswith("--"):
                    if _input == "--":
                        _optend = True
                        continue
                    _name = _input[2:]
                    if not (_name in self.__params.optparams):
                        print(f"ERROR: Unknown option: {_name}", file = _stderr)
                        return 1
                    _opt = self.__params.optparams[_name]
                # No! Assume it's the name of a shortcut
                else:
                    _short = _input[1:]
                    if not (_short in self.__params.shortcuts):
                        print(f"ERROR: Unknown shortcut: {_short}", file = _stderr)
                        return 1
                    _opt = self.__params.shortcuts[_short]
                # Add
                if isinstance(_opt, _CLIOptionWArg):
                    _optin = _opt.name
                else:
                    optargs.append(_opt.name)
                continue
            # If nothing else, consider it a required argument
            reqargs.append(_input)
        if _optin is not None:
            print("ERROR: Input ends before optional parameter value.", file = _stderr)
            return 1
        if len(reqargs) < len(self.__params.reqparams):
            print("ERROR: One or more required arguments are missing.", file = _stderr)
            return 1
        # Parse arguments
        for _i in range(len(self.__params.reqparams)):
            _input = reqargs[_i]
            _param = self.__params.reqparams[_i]
            _s, _r = _param.parse(_input)
            if not _s: return 1
            setattr(self, _param.name, _r)
        for _optarg in optargs:
            # Is this a flag
            if isinstance(_optarg, str):
                _param = self.__params.optparams[_optarg]
                setattr(self, _param.name, True)
            # No! This is a parameter.
            else:
                _param = _cast(_CLIOptionWArg, self.__params.optparams[_optarg[0]])
                _s, _r = _param.parse(_optarg[1])
                if not _s: return 1
                setattr(self, _param.name, _r)
        # Run main code
        return self._main()
    
    def _main(self) -> int:
        """
        Runs the main command code

        :return:
            Exit code
        """
        raise NotImplementedError()
        
    #endregion