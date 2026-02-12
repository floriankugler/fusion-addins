import importlib
import importlib.util
import json
import sys, os
from .runtime import RuntimeInfo

def run(context, addin_path: str):
    version = _load_version()
    addin_id = _load_id(addin_path)
    dev_mode = version == "dev"
    runtime_info = RuntimeInfo(dev_mode=dev_mode, version=version, id=addin_id)
    print(f"[INFO] Starting add-in. DEV_MODE={runtime_info.dev_mode}, VERSION={runtime_info.version}")
    if runtime_info.dev_mode:
        _reload_lib_modules()

    main = _load_main_module(addin_path, force_reload=runtime_info.dev_mode)
    main.run(context, runtime_info)

def stop(context, addin_path: str):
    version = _load_version()
    dev_mode = version == "dev"
    print(f"[INFO] Stopping add-in. DEV_MODE={dev_mode}, VERSION={version}")
    main = _load_main_module(addin_path)
    main.stop(context)

def _load_main_module(addin_path: str, force_reload: bool = False):
    addin_dir = os.path.abspath(os.path.dirname(addin_path))
    addin_name = os.path.basename(addin_dir)
    main_path = os.path.join(addin_dir, "main.py")
    module_name = f"fusion_addin_{addin_name}_main"

    module = sys.modules.get(module_name)
    if module and not force_reload and getattr(module, "__spec__", None):
        return module

    spec = importlib.util.spec_from_file_location(module_name, main_path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Failed to load add-in main module at {main_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def _load_id(addin_path: str) -> str:
    addin_dir = os.path.abspath(os.path.dirname(addin_path))
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
