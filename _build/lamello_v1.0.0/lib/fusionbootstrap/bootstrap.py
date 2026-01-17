import importlib
import json
import sys, os
from . import runtime

def run(context):
    runtime.VERSION = _load_version()
    runtime.ID = _load_id()
    runtime.DEV_MODE = runtime.VERSION == "dev"
    print(f"[INFO] Starting add-in. DEV_MODE={runtime.DEV_MODE}, VERSION={runtime.VERSION}")
    if runtime.DEV_MODE:
        _reload_lib_modules()

    main = importlib.import_module('main')
    if runtime.DEV_MODE:
        importlib.reload(main)
    main.run(context)

def stop(context):
    print(f"[INFO] Stopping add-in. DEV_MODE={runtime.DEV_MODE}, VERSION={runtime.VERSION}")
    main = importlib.import_module('main')
    main.stop(context)

def _load_id() -> str:
    bootstrap_dir = os.path.dirname(os.path.abspath(__file__))
    addin_dir = os.path.abspath(os.path.join(bootstrap_dir, "../.."))
    addin_name = os.path.basename(addin_dir)
    return f"com_floriankugler_{addin_name}"

def _load_version() -> str:
    """
    Load version from lib/__version__.py.
    Returns "dev" if __version__.py does not exist (development mode).
    """
    try:
        from lib import __version__ # type: ignore
        return getattr(__version__, "VERSION", "unknown")
    except ImportError:
        return "dev"

def _reload_lib_modules():
    """
    Force reload all imported modules under 'lib' in dev mode.
    Reload child modules before parent modules to reduce dependency issues.
    """
    # Collect all currently imported modules under 'lib'
    lib_modules = [name for name in sys.modules if name.startswith("lib.") and not name.startswith("lib.fusionbootstrap")]
    
    # Compute depth based on number of dots (more dots = deeper child)
    lib_modules.sort(key=lambda name: name.count('.'), reverse=True)

    for name in lib_modules:
        module = sys.modules.get(name)
        if module is not None:
            try:
                importlib.reload(module)
                print(f"[DEV_MODE] Reloaded {name}")
            except Exception as e:
                print(f"[DEV_MODE] Failed to reload {name}: {e}")
