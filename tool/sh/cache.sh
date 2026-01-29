# Clears the cache files

shdir="$(dirname $(realpath $BASH_SOURCE))"
pydir="$(dirname $shdir)/src"

clrcache() {
    local _dir=$1
    local _path=
    local _name=
    # Clear cache of sub-directories
    for _path in $_dir/*; do
        _name="$(basename $_path)"
        # Make sure path is directory
        if [ ! -d "$_path" ]; then continue; fi
        # Make sure this isn't a cache directory
        if [ "$_name" = "__pycache__" ]; then continue; fi
        # Clear cache
        clrcache $_path
    done
    # Delete cache
    _path="$_dir/__pycache__"
    if [ -d "$_path" ]; then
        rm -r $_path
    fi
}

clrcache $pydir