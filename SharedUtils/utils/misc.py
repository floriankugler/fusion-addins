from typing import Callable


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
        
