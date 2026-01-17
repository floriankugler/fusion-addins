#!/usr/bin/env bash
set -e

# Determine the directory of this script, resolving symlinks
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Repo root is assumed to be one level up from tools/
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ADDINS_SRC="$REPO_ROOT/addins-src"
LIB_DIR="$REPO_ROOT/lib"

echo "Creating dev symlinks for all add-ins in $ADDINS_SRC..."

for ADDIN_DIR in "$ADDINS_SRC"/*/; do
    ADDIN_NAME=$(basename "$ADDIN_DIR")
    LIB_LINK="$ADDIN_DIR/lib"

    echo "Processing add-in: $ADDIN_NAME"

    # Remove existing lib if it exists
    if [ -L "$LIB_LINK" ] || [ -e "$LIB_LINK" ]; then
        rm -rf "$LIB_LINK"
    fi

    # Create symlink to shared lib
    ln -s "$LIB_DIR" "$LIB_LINK"
    echo "  Linked lib/"
done

echo "All add-ins now have lib symlinked to repo-wide lib/"