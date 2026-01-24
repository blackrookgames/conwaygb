# Updates the _00 references

shdir="$(dirname $BASH_SOURCE)"
pydir="$(realpath $(dirname $(realpath $shdir)))"

update() {
    local _parent=$1
    local _relto=$2
    # _00.py
    local -a _00="$_parent/_00.py"
    # Delete _00 so it doesn't get detected when searching for python files
    if [ -f "$_00" ]; then
        rm "$_00"
    fi
    # Directories 
    local -a _dirs=()
    readarray -d '' _dirs < <(find "$_parent" -mindepth 1 -maxdepth 1 -type d -print0)
    # Python files
    local -a _pys=()
    readarray -d '' _pys < <(find "$_parent" -mindepth 1 -maxdepth 1 -type f -name '*.py' -print0)
    # Create _00
    local _path=""
    local _base=""
    local _name=""
    local -a _dir_pys=()
    for _path in "${_dirs[@]}"; do
        # Ensure directory is not python cache
        _base="$(basename "$_path")"
        if [ "$_base" = "__pycache__" ]; then
            continue
        fi
        # Ensure directory contains python code
        _dir_pys=()
        readarray -d '' _dir_pys < <(find "$_path" -mindepth 1 -type f -name '*.py' -print0)
        if [ "${#_dir_pys[@]}" -eq 0 ]; then
            continue
        fi
        # Add directory
        _name="$(realpath --relative-to="$_relto" "$_path")"
        _name="${_name//\//.}"
        echo "import $_name._00 as $_base" >>"$_00"
    done
    for _path in "${_pys[@]}"; do
        # Add file
        _name="$(realpath --relative-to="$_relto" "$_path")"
        _name="${_name%.*}"
        _name="${_name//\//.}"
        echo "from $_name import *" >>"$_00"
    done
    # Recursive
    for _path in "${_dirs[@]}"; do
        update "$_path" "$_relto"
    done
}

declare -a subdirs=()
readarray -d '' subdirs < <(find "$pydir" -mindepth 1 -maxdepth 1 -type d -print0)
for _subdir in "${subdirs[@]}"; do
    update "$_subdir" "$pydir"
done