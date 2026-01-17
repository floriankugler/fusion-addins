#!/usr/bin/env python3
import os, sys
import shutil
import json

# ============================
# Determine repo root relative to this script
# ============================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

ADDINS_SRC_DIR = os.path.join(REPO_ROOT, "addins-src")
LIB_SRC_DIR = os.path.join(REPO_ROOT, "lib")
BUILD_DIR = os.path.join(REPO_ROOT, "_build")

SEMANTIC_VERSION = "1.0.0"

# ============================
# Parse command line options
# ============================
FORCE_ALL_BREAKING = False
if "--all" in sys.argv:
    FORCE_ALL_BREAKING = True
    print("[INFO] --all specified: all add-ins will be considered breaking changes")
elif "--none" in sys.argv:
    FORCE_ALL_BREAKING = False
    print("[INFO] --none specified: no add-ins will be considered breaking changes")

# ============================
# Helper functions
# ============================
def copy_tree(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('.vscode', '.venv', '.env'))

def write_version_file(lib_dst, version_string):
    version_file = os.path.join(lib_dst, "__version__.py")
    with open(version_file, "w", encoding="utf-8") as f:
        f.write(f'VERSION = "{version_string}"\n')
    print(f"  Wrote {version_file}")

def ask_breaking_change(addin_name):
    if FORCE_ALL_BREAKING == False:
        return False
    elif FORCE_ALL_BREAKING == True:
        return True
    while True:
        resp = input(f"Add-in '{addin_name}': breaking change? [y/N]: ").strip().lower()
        if resp == "":
            return False
        if resp in ("y", "n"):
            return resp == "y"
        print("Please type 'y' or 'n' (or Enter for no).")

def vendor_addin(addin_name):
    # Ask user if this is a breaking change
    is_breaking = ask_breaking_change(addin_name)

    dst_addin_name = addin_name
    dst_addin_name += f"_v{SEMANTIC_VERSION.replace('.', '_')}"
    dst_addin = os.path.join(BUILD_DIR, dst_addin_name)
    src_addin = os.path.join(ADDINS_SRC_DIR, addin_name)

    print(f"\nVendoring {addin_name} → {dst_addin_name}")

    # Copy add-in files
    copy_tree(src_addin, dst_addin)
    shutil.move(os.path.join(dst_addin, f"{addin_name}.manifest"), os.path.join(dst_addin, f"{dst_addin_name}.manifest"))
    shutil.move(os.path.join(dst_addin, f"{addin_name}.py"), os.path.join(dst_addin, f"{dst_addin_name}.py"))

    # Copy shared lib
    lib_dst = os.path.join(dst_addin, "lib")
    copy_tree(LIB_SRC_DIR, lib_dst)

    # Write version file in lib
    write_version_file(lib_dst, SEMANTIC_VERSION)

    # Update manifest
    manifest_path = os.path.join(dst_addin, f"{addin_name}.manifest")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # Update version
        manifest["version"] = SEMANTIC_VERSION

        # Update ID if breaking change
        if is_breaking:
            manifest["id"] = f"com.floriankugler.{addin_name}_v{SEMANTIC_VERSION}"

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        print(f"  Updated manifest version: {SEMANTIC_VERSION}")
        if is_breaking:
            print(f"  Updated manifest ID for breaking change: {manifest['id']}")

# ============================
# Main
# ============================
if __name__ == "__main__":
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR, exist_ok=True)

    for addin_name in os.listdir(ADDINS_SRC_DIR):
        addin_path = os.path.join(ADDINS_SRC_DIR, addin_name)
        if os.path.isdir(addin_path):
            vendor_addin(addin_name)

    print("\nVendoring complete.")
