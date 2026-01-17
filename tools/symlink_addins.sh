#!/usr/bin/env bash
set -e

# ============================
# CONFIG
# ============================

# Determine the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Repo root (assumes script is in tools/)
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ADDINS_SRC="$REPO_ROOT/_build"

# Check for --dev flag
for arg in "$@"; do
    if [ "$arg" == "--dev" ]; then
        ADDINS_SRC="$REPO_ROOT/addins-src"
        echo "Development mode: using source files."
        break
    fi
done

# Fusion 360 AddIns folder (macOS)
FUSION_ADDINS="$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns"

# ============================
# SYMLINK ADDINS
# ============================

echo "Linking all add-ins from $ADDINS_SRC into Fusion 360 AddIns folder..."
mkdir -p "$FUSION_ADDINS"

for ADDIN_DIR in "$ADDINS_SRC"/*/; do
    ADDIN_NAME=$(basename "$ADDIN_DIR")
    LINK_PATH="$FUSION_ADDINS/$ADDIN_NAME"

    echo "Processing add-in: $ADDIN_NAME"

    # Remove existing link if it exists
    if [ -L "$LINK_PATH" ] || [ -e "$LINK_PATH" ]; then
        rm -rf "$LINK_PATH"
    fi

    # Create symlink
    ln -s "$ADDIN_DIR" "$LINK_PATH"
    echo "  Linked $LINK_PATH -> $ADDIN_DIR"
done

echo "All add-ins are now symlinked into Fusion 360."
