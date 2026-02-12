import functools, math
import adsk.core, adsk.fusion
from typing import cast
from lib import custom_compute_feature, utils, combine, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo
from Shared import CoordinateSystem, PatternInputs
import Triangles, Rhombuses, Cross, RoundedRectangle, Froli

_feature: custom_compute_feature.CustomComputeFeature

def run(context, runtime_info: RuntimeInfo):
    global _feature
    if runtime_info.dev_mode:
        utils.misc.force_reload_modules('Shared', 'Triangles', 'Rhombuses', 'Cross', 'RoundedRectangle', 'Froli')
    _feature = PatternCutout(runtime_info)

def stop(context):
    global _feature
    del _feature


class PatternCutout(custom_compute_feature.CustomComputeFeature):
    inputs: PatternInputs
    
    @property
    def plugin_name(self) -> str:
        return 'PatternCutouts'

    @property
    def plugin_desc(self) -> str:
        return 'Pattern Cutouts'

    @property
    def plugin_tooltip(self) -> str:
        return 'Creates patterned cutouts of various shapes.'
    
    def get_ui_placement(self) -> ui_placement.UIPlacement:
        section = ui_placement.PlacementSpec(
            id='SeparatorBeforeCustomAddins',
            anchor_id='FusionMoveCommand',
            insert_before=True,
        )
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id=section.id,
            insert_before=True,
        )
        return ui_placement.UIPlacement(
            panel_id='SolidModifyPanel',
            command=command,
            section=section,
        )

    def create_inputs(self) -> PatternInputs:
        return PatternInputs(self.app.activeProduct.unitsManager)

    def execute(self) -> list[combine.Combine]:
        result: list[combine.Combine] = []
        for face in cast(list[adsk.fusion.BRepFace], self.inputs.faces.value):
            mgr = adsk.fusion.TemporaryBRepManager.get()
            opposite_face = utils.brep.get_opposite_face(face)
            cut = utils.brep.normal_towards_face(face, opposite_face)
            cut.scaleBy(utils.brep.get_board_thickness(face) - self.inputs.remainder.value)

            shape = self.create_patterns_for_face(face, cut)
            if not shape:
                continue

            # Apply fillets to all non-smooth edges
            if self.inputs.fillet.value > 0:
                non_smooth_edges = (e for e in shape.edges if utils.brep.is_parallel(e, cut) and not utils.brep.is_smooth_edge(e))
                if next(non_smooth_edges, None):
                    temp_base = self.component.features.baseFeatures.add()
                    temp_base.startEdit()
                    self.component.bRepBodies.add(shape, temp_base)
                    base_body = temp_base.bodies[0]
                    fillet_edges = [e for e in base_body.edges if utils.brep.is_parallel(e, cut) and not utils.brep.is_smooth_edge(e)]
                    fillet_input = self.component.features.filletFeatures.createInput()
                    objs = adsk.core.ObjectCollection.createWithArray(cast(list[adsk.core.Base], fillet_edges))
                    fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(objs, adsk.core.ValueInput.createByReal(self.inputs.fillet.value), False)
                    fillet_input.targetBaseFeature = temp_base
                    self.component.features.filletFeatures.add(fillet_input)
                    shape = mgr.copy(base_body)                    
                    temp_base.finishEdit()
                    temp_base.deleteMe()

            result.append(combine.Combine(face.body, shape, combine.Operation.CUT))
        return result
    
    def create_patterns_for_face(self, face: adsk.fusion.BRepFace, cut: adsk.core.Vector3D) -> adsk.fusion.BRepBody | None:
        mgr = adsk.fusion.TemporaryBRepManager.get()
        profiles = cast(list[adsk.fusion.Profile], self.inputs.profiles.value)
        scope_edges = cast(list[adsk.fusion.BRepEdge], self.inputs.scope.value)
        axis: adsk.core.Vector3D | None = None
        if self.inputs.axis.value:
            orig_axis = cast(adsk.fusion.BRepEdge, self.inputs.axis.value[0])
            axis_vector = utils.brep.normal_along_edge(orig_axis)
            coords = utils.brep.coordinate_system_around_face(face, cut)
            u = coords[1].dotProduct(axis_vector)
            v = coords[2].dotProduct(axis_vector)
            axis = utils.vector.add(utils.vector.scaled_by(coords[1], u), utils.vector.scaled_by(coords[2], v))
        
        if not profiles and not scope_edges:
            return self.create_pattern_for_face(face, cut, axis)

        result: list[adsk.fusion.BRepBody] = []
        for profile in profiles:
            profile_body = utils.brep.create_body_from_profile(profile)
            profile_face = profile_body.faces[0]
            height = utils.vector.scaled_by(utils.vector.normalized(cut), 100_000)
            volumetric_profile_body = utils.brep.create_body_from_face(profile_face, height)
            mgr.transform(volumetric_profile_body, utils.matrix.translation_matrix(utils.vector.scaled_by(height, -0.5)))
            face_body_copy = mgr.copy(face.body)
            mgr.booleanOperation(face_body_copy, volumetric_profile_body, adsk.fusion.BooleanTypes.IntersectionBooleanType) # type: ignore
            pattern_faces = [f for f in face_body_copy.faces if utils.brep.is_co_planar(face, f)]
            pattern_faces.sort(key=lambda f: f.area, reverse=True)
            pattern_face = pattern_faces[0] if pattern_faces else None
            if not pattern_face:
                continue
            result.append(self.create_pattern_for_face(pattern_face, cut, axis))

        if scope_edges:
            measure = adsk.core.Application.get().measureManager
            coords = utils.brep.coordinate_system_around_face(face, cut, axis)
            scope_bbs = [measure.getOrientedBoundingBox(e, coords[1], coords[2]) for e in scope_edges]
            scope_bb = functools.reduce(lambda bb1, bb2: utils.fusion.oriented_boundig_box_union(bb1, bb2), scope_bbs[1:], scope_bbs[0])
            scope_bb.height = 100_000
            try:
                scope_body = mgr.createBox(scope_bb)
                face_body_copy = mgr.copy(face.body)
                mgr.booleanOperation(face_body_copy, scope_body, adsk.fusion.BooleanTypes.IntersectionBooleanType) # type: ignore
                pattern_faces = [f for f in face_body_copy.faces if utils.brep.is_co_planar(face, f)]
                pattern_faces.sort(key=lambda f: f.area, reverse=True)
                pattern_face = pattern_faces[0] if pattern_faces else None
                if pattern_face:
                    result.append(self.create_pattern_for_face(pattern_face, cut, axis))
            except:
                pass
        
        return utils.brep.union(result) if result else None
            
    def create_pattern_for_face(self, face: adsk.fusion.BRepFace, cut: adsk.core.Vector3D, axis: adsk.core.Vector3D | None) -> adsk.fusion.BRepBody:
        mgr = adsk.fusion.TemporaryBRepManager.get()
        coords = utils.brep.coordinate_system_around_face(face, cut, axis)
        shape = self.call_generator(face, coords)
        mgr.transform(shape, utils.matrix.transform_from_root(*coords[:3]))

        # Early exit for simple rectangles
        if utils.brep.is_rectangular_face(face) and not axis:
            return shape

        # Start base feature for temporary offsetting operations. This will be deleted afterwards.
        temp_base = self.component.features.baseFeatures.add()
        temp_base.startEdit()
        self.component.bRepBodies.add(face.body, temp_base)
        base_body = temp_base.bodies[0]
        base_face = next((f for f in base_body.faces if f.boundingBox.minPoint.isEqualTo(face.boundingBox.minPoint) and f.boundingBox.maxPoint.isEqualTo(face.boundingBox.maxPoint)))

        # Create sketch to offset all loops
        sketch = self.component.sketches.addToBaseOrFormFeature(base_face, temp_base, includeFaceEdges=False)
        for loop in base_face.loops:
            loop_edges = cast(list[adsk.core.Base], utils.fusion.as_list(loop.edges))
            entities = cast(list[adsk.fusion.SketchCurve], list(sketch.project2(loop_edges, False)))
            offset_value = self.inputs.inset.value if loop.isOuter else self.inputs.inner_loop_offset.value
            if offset_value != 0:
                sketch.setConstructionState(entities, adsk.fusion.SketchCurveConstructionStates.ConstructionSketchCurveConstructionState) # type: ignore
            else:   
                continue
            # curves = cast(list[adsk.fusion.SketchCurve], utils.fusion.as_list(sketch.findConnectedCurves(entities[0])))
            sign = -1 if utils.brep.are_sketch_curves_right_handed(entities, base_face) else 1
            if loop.isOuter and loop.edges.count == 1: # special case for outer loops with a single edge (circle)
                sign *= -1
            input = sketch.geometricConstraints.createOffsetInput(entities, adsk.core.ValueInput.createByReal(offset_value * sign))
            input.isTopologyMatched = False
            sketch.geometricConstraints.addOffset2(input)

        # Find largest profile in sketch, create a body from the profile and intersect with the cut body
        sorted_profiles = sorted(utils.fusion.as_list(sketch.profiles), key=lambda p: p.areaProperties().area, reverse=True)
        offset_profile = sorted_profiles[0]
        offset_start_face = offset_profile.face
        mgr.transform(offset_start_face.body, utils.matrix.transform_from_root(sketch.origin, sketch.xDirection, sketch.yDirection))
        offset_body = utils.brep.create_body_from_face(offset_start_face, cut)
        mgr.booleanOperation(shape, offset_body, adsk.fusion.BooleanTypes.IntersectionBooleanType) # type: ignore

        temp_base.finishEdit()
        temp_base.deleteMe()

        # Create tabs for inner loops
        if self.inputs.tabs.value and self.inputs.is_control_visible(self.inputs.tabs):
            measure = adsk.core.Application.get().measureManager
            xn, yn = utils.vector.normalized(coords[1]), utils.vector.normalized(coords[2])
            outer_loop = utils.brep.outer_edges_of_face(face)
            inner_loops = [l for l in face.loops if not l.isOuter]
            for loop in inner_loops:
                center = utils.vector.scaled_by(utils.vector.add(loop.boundingBox.minPoint.asVector(), loop.boundingBox.maxPoint.asVector()), 0.5).asPoint()
                connections: list[adsk.core.Vector3D] = []
                for edge in outer_loop:
                    _, param_on_edge = edge.evaluator.getParameterAtPoint(center)
                    _, min_param, max_param = edge.evaluator.getParameterExtents()
                    if param_on_edge < min_param or param_on_edge > max_param:
                        continue
                    _, point_on_edge = edge.evaluator.getPointAtParameter(param_on_edge)
                    loop_to_edge = utils.vector.subtract(point_on_edge.asVector(), center.asVector())
                    connections.append(loop_to_edge)
                connections.sort(key=lambda v: v.length)

                connection = connections[0]
                along_edge = cut.crossProduct(connection)
                bb = measure.getOrientedBoundingBox(loop, along_edge, connection)
                tab_width = bb.length + 2*self.inputs.inner_loop_offset.value
                tab = utils.brep.rectangle(connection.length, tab_width, cut.length)
                positioned_tab = utils.brep.transformed(tab, utils.matrix.combine_transforms([
                    utils.matrix.translation_matrix(adsk.core.Vector3D.create(connection.length/2, 0, 0)),
                    utils.matrix.transform_from_root(center, connection, along_edge),
                ]))
                mgr.booleanOperation(shape, positioned_tab, adsk.fusion.BooleanTypes.DifferenceBooleanType) # type: ignore
        
        # Re-create the cut body ommitting small lumps that would probably fail on filletting
        min_lump_volume = math.pow(self.inputs.fillet.value * 2, 2) * cut.length * 3
        shape_def = utils.brep.body_definition(shape, include_lump=lambda l: l.volume >= min_lump_volume)
        shape = shape_def.createBody()

        return shape

        
    def call_generator(self, face: adsk.fusion.BRepFace, coords: CoordinateSystem) -> adsk.fusion.BRepBody:
        match self.inputs.type.value:
            case PatternInputs.TRIANGLES.value:
                return Triangles.create_triangles_from_inputs(coords, self.inputs)
            case PatternInputs.RHOMBUSES.value:
                return Rhombuses.create_rhombuses_from_inputs(coords, self.inputs)
            case PatternInputs.CROSS.value:
                return Cross.create_cross_from_inputs(coords, self.inputs)
            case PatternInputs.ROUNDED_RECTANGLE.value:
                return RoundedRectangle.create_rounded_rectangle_from_inputs(coords, self.inputs)
            case PatternInputs.FROLI.value:
                return Froli.create_froli_from_inputs(coords, self.inputs)
            case _:
                raise ValueError(f'Unknown pattern type: {self.inputs.type.value}')
                
    def input_changed(self, input):
        if input.id == self.inputs.type.id:
            self.inputs.update_visibilities()
