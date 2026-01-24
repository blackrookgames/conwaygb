# Clears the cache files

shdir="$(dirname $BASH_SOURCE)"
pydir="$(dirname $shdir)"

readarray -d '' dirs < <(find "$pydir" -type d -name __pycache__ -print0)
for path in "${dirs[@]}"; do
    rm -r $path
done