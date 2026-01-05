from dataclasses import dataclass
import math
import adsk.fusion
from adsk.core import Point3D, Vector3D
import utils
from enum import Enum, unique

@unique
class Type(Enum):
    CLAMEX_P10 = 10
    CLAMEX_P14 = 14
    CABINEO_8 = 8
    CABINEO_12 = 12
    CABINEO_8_M6 = 9        

    @property
    def is_clamex(self) -> bool:
        return self in [Type.CLAMEX_P10, Type.CLAMEX_P14]
    
    @property
    def is_cabineo(self) -> bool:
        return not self.is_clamex

@unique
class Insert(Enum):
    M6x123 = 1
    M6x153 = 2
    HAEFELE_EINDREHMUFFE_10x8 = 3

def create_clamex_access_hole(type: Type, thickness: float) -> adsk.fusion.BRepBody:
    access_depth = thickness/2
    access_hole_radius = 0.6/2
    access_edge_distance = 0.75
    if type == Type.CLAMEX_P14:
        cyl = utils.brep.cylinder(access_hole_radius, -access_depth)
        return utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(0, access_edge_distance, 0)))
    else:
        return utils.brep.transformed(
            utils.brep.slot(0.25, access_hole_radius, access_depth), 
            utils.matrix.combine_transforms([
                utils.matrix.rotation_matrix(-math.pi/2, Vector3D.create(0, 0, 1), Point3D.create(0, 0, 0)),
                utils.matrix.translation_matrix(Vector3D.create(0, access_edge_distance, -access_depth))
            ])
        )
    
def create_clamex_guide_holes(access_thickness: float, guide_thickness: float, through: bool) -> adsk.fusion.BRepBody:
    guide_hole_depth = guide_thickness if through else 0.8
    guide_hole_radius = 0.77/2
    guide_hole_distance = 10.1
    guide_hole_edge_distance = access_thickness/2
    cyl = utils.brep.cylinder(guide_hole_radius, guide_hole_depth)
    guide_hole = utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(guide_hole_distance/2, guide_hole_edge_distance, 0)))
    return utils.brep.union([
        guide_hole,
        utils.brep.transformed(guide_hole, utils.matrix.translation_matrix(Vector3D.create(-guide_hole_distance, 0, 0)))
    ])

def create_cabineo_connector_hole(flush: bool) -> adsk.fusion.BRepBody:
    depth = 1.15 if flush else 1.1
    cyl = utils.brep.cylinder(1.5/2, -depth)
    triple_holes = utils.brep.union([
        utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(0, 0.36, 0))),
        utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(0, 1.48, 0))),
        utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(0, 2.6, 0))),
    ])
    if not flush:
        return triple_holes
    inset = 0.08
    return utils.brep.union([
        triple_holes,
        utils.brep.transformed(
            utils.brep.cylinder(1.67/2, -inset),
            utils.matrix.translation_matrix(Vector3D.create(0, 2.6, 0))
        ),
        utils.brep.transformed(
            utils.brep.rectangle(1.67, 2.6, inset),
            utils.matrix.translation_matrix(Vector3D.create(0, 2.6/2, -inset))
        )
    ])

def create_cabineo_screw_hole(type: Type, insert: Insert | None, guide_thickness: float, flush: bool, through: bool) -> adsk.fusion.BRepBody:
    edge_distance = (0.5+0.08) if flush else 0.5
    depth: float
    diameter = 0.5
    if type == Type.CABINEO_8:
        depth = 0.8
    elif type == Type.CABINEO_12:
        depth = 1.2
    else:
        diameter = 0.8
        if insert == Insert.M6x123:
            depth = 1.35
        elif insert == Insert.M6x153:
            depth = 1.65
        elif insert == Insert.HAEFELE_EINDREHMUFFE_10x8:
            depth = 0.85
    if through:
        depth = guide_thickness
    return utils.brep.transformed(
        utils.brep.cylinder(diameter/2, depth),
        utils.matrix.translation_matrix(Vector3D.create(0, edge_distance, 0))
    )

@dataclass
class Params:
    type: Type
    insert: Insert | None = None
    flush: bool = True
    through: bool = False

def create_hole_bodies(points: list[Vector3D], edge: adsk.fusion.BRepEdge, access_face: adsk.fusion.BRepFace, slot_face: adsk.fusion.BRepFace, guide_face: adsk.fusion.BRepFace, params: Params) -> tuple[adsk.fusion.BRepBody, adsk.fusion.BRepBody]:
    access_thickness = utils.brep.get_board_thickness(access_face)
    guide_thickness = utils.brep.get_board_thickness(guide_face)

    access_shape: adsk.fusion.BRepBody
    guide_shape: adsk.fusion.BRepBody

    if params.type.is_clamex:
        access_shape = create_clamex_access_hole(params.type, access_thickness)
        guide_shape = create_clamex_guide_holes(access_thickness, guide_thickness, params.through)
    else:
        access_shape = create_cabineo_connector_hole(params.flush)
        guide_shape = create_cabineo_screw_hole(params.type, params.insert, guide_thickness, params.flush, params.through)

    access_bodies = utils.brep.place_body_on_face_at_positions(access_shape, access_face, edge, points)
    guide_bodies = utils.brep.place_body_on_face_at_positions(guide_shape, slot_face, edge, points)
    return access_bodies, guide_bodies