# Updates the __init__ references

shdir="$(dirname $(realpath $BASH_SOURCE))"
pydir="$(dirname $shdir)/src"

updateinit() {
    local _dir=$1
    local _path=
    local _name=
    local _ext=
    # Gather files/directories
    local -a _files=()
    local -a _dirs=()
    for _path in $_dir/*; do
        _name="$(basename $_path)"
        # Is it a file?
        if [ -f "$_path" ]; then
            # Make sure it is a .py file
            _ext="${_path##*.}"
            if [ ! "$_ext" = "py" ]; then continue ; fi
            _name="${_name%.*}"
            # Make sure it isn't a init file
            if [ "$_name" = "__init__" ]; then continue ; fi
            # Add file
            _files+=("$_name")
        # Is it a directory?
        elif [ -d "$_path" ]; then
            # Make sure it isn't a cache directory
            if [ "$_name" = "__pycache__" ]; then continue ; fi
            # Update
            updateinit $_path
            # Add directory
            _dirs+=("$_name")
        fi
    done
    # Create init
    local _init="$_dir/__init__.py"
    if [ -f "$_init" ]; then rm -f "$_init" ; fi
    # Loop thru directories
    for _name in "${_dirs[@]}"; do
        echo "from .$_name import *" >>"$_init"
    done
    # Loop thru files
    for _name in "${_files[@]}"; do
        echo "from .$_name import *" >>"$_init"
    done
}

updateinit $pydir