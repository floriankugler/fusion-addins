from typing import Callable, Optional, cast
import adsk.core, adsk.fusion
from adsk.core import Point3D
from . import vector
import traceback, inspect


def as_list(objs):
    return [objs.item(idx) for idx in range(objs.count)]

def as_object_collection(objs):
    return adsk.core.ObjectCollection.createWithArray(as_list(objs))

def traverse_occurrence_tree(occurence: Optional[adsk.fusion.Occurrence], process: Callable[[adsk.fusion.Occurrence | adsk.fusion.Component], bool]):
    """
    Traverses the occurrence tree, starting with occurrence, going depth first, then siblings, then up to parent and so on until the root is reached.

    occurence : The occurrence to start the search from. If None, starts from the root component.
    process : A function that takes an occurrence or the root component and returns True to stop the search, False to continue.
    """
    previous = None
    design = cast(adsk.fusion.Design, adsk.core.Application.get().activeProduct)
    root_component = design.rootComponent
    current: adsk.fusion.Occurrence | adsk.fusion.Component = occurence or root_component

    def search_down(occ) -> bool:
        # Search this component first
        if process(occ):
            return True

        # Recurse into children (occurrences)
        children = []
        if isinstance(occ, adsk.fusion.Occurrence):
            children = occ.childOccurrences
        else:
             children = occ.occurrences  # Root component case
        for occ in children:
            if occ == previous:
                continue
            if search_down(occ):
                return True

        return False

    while current:
        # 1. Search current + children
        if search_down(current):
            return 

        if current == root_component:
            break

        # 2. Move up to parent
        assert(isinstance(current, adsk.fusion.Occurrence))
        occ_ctx = current.assemblyContext
        child_occurrences = None
        if not occ_ctx:
            root = current.component.parentDesign.rootComponent
            child_occurrences = root.occurrences
            parent = root
        else:
            parent = occ_ctx
            child_occurrences = parent.childOccurrences       

        # 3. Search siblings in parent
        for sibling_occ in child_occurrences:
            if sibling_occ == current:
                continue
            if search_down(sibling_occ):
                return

        previous = current
        current = parent

    return None

def point_to_str(point: Point3D) -> str:
    return f'{point.x};{point.y};{point.z}'
    
def str_to_point(str: str) -> Point3D:
    comps = [float(x) for x in str.split(';')]
    return Point3D.create(comps[0], comps[1], comps[2])

def new_event_handler(handler, superclass):
	class EventHandler(superclass):
		def notify(self, eventArgs):
			try:
				handler(eventArgs)
			except:
				handleException()
	return EventHandler()

def log(message):
    userInterface = adsk.core.Application.get().userInterface
    textPalette = cast(adsk.core.TextCommandPalette, userInterface.palettes.itemById('TextCommands'))
    textPalette.writeText(message)

def handleException():
	frameInfo = inspect.stack()[1]
	prefix = ''
	if 'self' in frameInfo.frame.f_locals:
		prefix = frameInfo.frame.f_locals['self'].__class__.__name__ + '.'
	log(f'{prefix}{frameInfo.function}: {traceback.format_exc()}\n')

def oriented_boundig_box_union(b1: adsk.core.OrientedBoundingBox3D, b2: adsk.core.OrientedBoundingBox3D) -> adsk.core.OrientedBoundingBox3D:
    """
    Creates a new oriented bounding box, using the length and width direction of the first one, that contains both input bounding boxes.
    """
    lv = b1.lengthDirection
    wv = b1.widthDirection
    hv = lv.crossProduct(wv)
    
    b1_l_min = vector.add(b1.centerPoint.asVector(), vector.scaled_by(lv, -b1.length/2)).dotProduct(lv)
    b1_l_max = vector.add(b1.centerPoint.asVector(), vector.scaled_by(lv, b1.length/2)).dotProduct(lv)
    b1_w_min = vector.add(b1.centerPoint.asVector(), vector.scaled_by(wv, -b1.width/2)).dotProduct(wv)
    b1_w_max = vector.add(b1.centerPoint.asVector(), vector.scaled_by(wv, b1.width/2)).dotProduct(wv)
    b1_h_min = vector.add(b1.centerPoint.asVector(), vector.scaled_by(hv, -b1.height/2)).dotProduct(hv)
    b1_h_max = vector.add(b1.centerPoint.asVector(), vector.scaled_by(hv, b1.height/2)).dotProduct(hv)

    b2_l_min = vector.add(b2.centerPoint.asVector(), vector.scaled_by(b2.lengthDirection, -b2.length/2)).dotProduct(lv)
    b2_l_max = vector.add(b2.centerPoint.asVector(), vector.scaled_by(b2.lengthDirection, b2.length/2)).dotProduct(lv)
    b2_w_min = vector.add(b2.centerPoint.asVector(), vector.scaled_by(b2.widthDirection, -b2.width/2)).dotProduct(wv)
    b2_w_max = vector.add(b2.centerPoint.asVector(), vector.scaled_by(b2.widthDirection, b2.width/2)).dotProduct(wv)
    b2_h_min = vector.add(b2.centerPoint.asVector(), vector.scaled_by(b2.lengthDirection.crossProduct(b2.widthDirection), -b2.height/2)).dotProduct(hv)
    b2_h_max = vector.add(b2.centerPoint.asVector(), vector.scaled_by(b2.lengthDirection.crossProduct(b2.widthDirection), b2.height/2)).dotProduct(hv)

    l_min = min(b1_l_min, b2_l_min)
    l_max = max(b1_l_max, b2_l_max)
    w_min = min(b1_w_min, b2_w_min)
    w_max = max(b1_w_max, b2_w_max)
    h_min = min(b1_h_min, b2_h_min)
    h_max = max(b1_h_max, b2_h_max)

    center = vector.scaled_by(lv, (l_min + l_max) / 2)
    center.add(vector.scaled_by(wv, (w_min + w_max) / 2))
    center.add(vector.scaled_by(hv, (h_min + h_max) / 2))

    return adsk.core.OrientedBoundingBox3D.create(center.asPoint(), lv, wv, l_max - l_min, w_max - w_min, h_max - h_min)