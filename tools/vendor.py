#!/usr/bin/env python3
import os, sys
import shutil
import json
import re

# ============================
# Determine repo root relative to this script
# ============================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

ADDINS_SRC_DIR = os.path.join(REPO_ROOT, "addins-src")
LIB_SRC_DIR = os.path.join(REPO_ROOT, "lib")
BUILD_DIR = os.path.join(REPO_ROOT, "_build")
LIB_VERSION_FILE = os.path.join(LIB_SRC_DIR, "version.json")

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

def load_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def version_suffix(version_string):
    # Keep artifact names filesystem-friendly and deterministic.
    return re.sub(r"[^A-Za-z0-9]+", "_", version_string).strip("_")

def strip_id_suffix(manifest_id):
    return re.sub(r"_i\d+_l\d+$", "", manifest_id)

def vendor_addin(addin_name, lib_version, lib_api_epoch):
    src_addin = os.path.join(ADDINS_SRC_DIR, addin_name)
    addin_version_path = os.path.join(src_addin, "version.json")
    if not os.path.exists(addin_version_path):
        raise FileNotFoundError(f"Missing add-in version file: {addin_version_path}")

    addin_version_meta = load_json_file(addin_version_path)
    addin_version = addin_version_meta["addin_version"]
    interface_epoch = int(addin_version_meta["interface_epoch"])
    requires_lib_api_epoch = int(addin_version_meta["requires_lib_api_epoch"])

    if requires_lib_api_epoch != lib_api_epoch:
        raise RuntimeError(
            f"Add-in '{addin_name}' requires lib API epoch {requires_lib_api_epoch}, "
            f"but lib/version.json declares {lib_api_epoch}."
        )

    combined_version = f"{addin_version}+lib{lib_version}"
    dst_addin_name = addin_name
    dst_addin_name += f"_v{version_suffix(combined_version)}"
    dst_addin = os.path.join(BUILD_DIR, dst_addin_name)

    print(f"\nVendoring {addin_name} → {dst_addin_name}")

    # Copy add-in files
    copy_tree(src_addin, dst_addin)
    shutil.move(os.path.join(dst_addin, f"{addin_name}.manifest"), os.path.join(dst_addin, f"{dst_addin_name}.manifest"))
    shutil.move(os.path.join(dst_addin, f"{addin_name}.py"), os.path.join(dst_addin, f"{dst_addin_name}.py"))

    # Copy shared lib
    lib_dst = os.path.join(dst_addin, "lib")
    copy_tree(LIB_SRC_DIR, lib_dst)

    # Write version file in lib
    write_version_file(lib_dst, combined_version)

    # Update manifest
    manifest_path = os.path.join(dst_addin, f"{dst_addin_name}.manifest")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # Set deterministic, strictly coupled ID and version metadata.
        base_id = strip_id_suffix(manifest["id"])
        manifest["id"] = f"{base_id}_i{interface_epoch}_l{lib_api_epoch}"
        manifest["version"] = combined_version

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        print(f"  Updated manifest version: {manifest['version']}")
        print(f"  Updated manifest id: {manifest['id']}")

# ============================
# Main
# ============================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Usage: python3 tools/vendor.py")
        print("Versioning is configured through addins-src/*/version.json and lib/version.json.")
        sys.exit(2)

    if not os.path.exists(LIB_VERSION_FILE):
        raise FileNotFoundError(f"Missing lib version file: {LIB_VERSION_FILE}")
    lib_version_meta = load_json_file(LIB_VERSION_FILE)
    lib_version = lib_version_meta["lib_version"]
    lib_api_epoch = int(lib_version_meta["lib_api_epoch"])

    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR, exist_ok=True)

    for addin_name in sorted(os.listdir(ADDINS_SRC_DIR)):
        addin_path = os.path.join(ADDINS_SRC_DIR, addin_name)
        if os.path.isdir(addin_path):
            vendor_addin(addin_name, lib_version, lib_api_epoch)

    print("\nVendoring complete.")
