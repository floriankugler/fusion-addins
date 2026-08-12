import sys, importlib
from typing import Callable, Any

def force_reload_modules(*module_names):
    """Force reloads specified modules if they are already in memory."""
    for name in module_names:
        if name in sys.modules:
            importlib.reload(sys.modules[name])

def intersect_lists(l1: list, l2: list) -> list:
    result = []
    for x in l2:
        if x in l1:
            result.append(x)
    return result

def list_contains_by_identity(list, obj):
    for x in list:
        if x == obj:
            return True
    return False

def binary_search(lower_bound: float, upper_bound: float, compute: Callable[[float], float], target: float, tolerance: float) -> float:
    lower = lower_bound
    upper = upper_bound
    mid = (upper + lower) / 2
    value = compute(mid)
    while abs(value - target) > tolerance:
        if value > target:
            upper = mid
        else:
            lower = mid
        mid = (upper + lower) / 2
        new_value = compute(mid)
        if abs(new_value - value) < 1e-6:
            break
        value = new_value
    return mid
        
def is_instance(value, cls) -> bool:
    """isinstance that survives a dev-mode module reload.

    All add-ins share one 'lib' package, and starting any add-in in dev mode
    reloads lib.*, which replaces every class object in it. Add-in modules
    imported before that reload keep instances of the PREVIOUS class, so a
    plain isinstance against the current class returns False even though the
    object is the same kind of thing. Falling back to a module+qualname match
    keeps those objects usable until the add-in itself is reloaded.
    """
    if isinstance(value, cls):
        return True
    try:
        return any(
            base.__module__ == cls.__module__
            and base.__qualname__ == cls.__qualname__
            for base in type(value).__mro__
        )
    except AttributeError:
        return False

def class_property_values(cls, type) -> list[Any]:
    return [value for key, value in cls.__dict__.items() if not key.startswith('__') and (type is None or is_instance(value, type))]

def float_range(start, stop, step):
    while start < stop:
        yield round(start, 10) # Rounding prevents floating point drift
        start += step