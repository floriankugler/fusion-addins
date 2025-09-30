from typing import Any, Callable
import adsk.core, adsk.fusion
from adsk.core import Point3D
from . import misc


def as_object_collection(objs):
    coll = adsk.core.ObjectCollection.create()
    for body in misc.as_list(objs):
        coll.add(body)
    return coll

def get_base_feature(custom_feature: adsk.fusion.CustomFeature) -> adsk.fusion.BaseFeature:
    for feature in custom_feature.features:
        if feature.objectType == adsk.fusion.BaseFeature.classType():
            return feature

def traverse_occurrence_tree(occurence: adsk.fusion.Occurrence, process: Callable[[adsk.fusion.Occurrence], bool]):
    def search_down(occ: adsk.fusion.Occurrence) -> bool:
        # Search this component first
        if process(occ):
            return True

        # Recurse into children (occurrences)
        for occ in occ.childOccurrences:
            if search_down(occ):
                return True

        return False

    current = occurence
    while current:
        # 1. Search current + children
        if search_down(current):
            return 

        # 2. Move up to parent
        occ_ctx = current.assemblyContext
        if not occ_ctx:
            break  # at root
        parent = occ_ctx

        # 3. Search siblings in parent
        for sibling_occ in parent.childOccurrences:
            if sibling_occ == current:
                continue
            if search_down(sibling_occ):
                return

        current = parent

    return None

def point_to_str(point: Point3D) -> str:
    return f'{point.x};{point.y};{point.z}'
    
def str_to_point(str: str) -> Point3D:
    comps = [float(x) for x in str.split(';')]
    return Point3D.create(comps[0], comps[1], comps[2])


