from lib import custom_compute_feature, inputs, combine, errors, utils, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from typing import cast

_feature: custom_compute_feature.CustomComputeFeature | None = None
DEBUG_KEEP_RESULT_SKETCH = False


def run(context, runtime_info: RuntimeInfo):
    global _feature
    _feature = TransferShape(runtime_info)


def stop(context):
    global _feature
    if _feature:
        _feature.shutdown()
    _feature = None


class TransferShapeInputs(inputs.Inputs):
    class Operations:
        JOIN = inputs.DropDownInput.Item("Join", 0)
        CUT = inputs.DropDownInput.Item("Cut", 1)
        INTERSECT = inputs.DropDownInput.Item("Intersect", 2)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.target_face = inputs.SelectionByEntityTokenInput(
            id="targetFace",
            name="Target Face",
            filter=["PlanarFaces"],
            lower_bound=1,
            upper_bound=1,
            tool_tip="Select the planar face of the body to modify.",
        )
        self.base_sketch = inputs.SelectionByEntityTokenInput(
            id="baseSketch",
            name="Base Sketch",
            filter=["Sketches"],
            lower_bound=1,
            upper_bound=1,
            tool_tip="Select a sketch that lies on the selected target face.",
        )
        self.intersect_faces = inputs.SelectionByEntityTokenInput(
            id="intersectFaces",
            name="Intersect Faces",
            filter=["Faces"],
            lower_bound=0,
            upper_bound=0,
            tool_tip="Select faces to intersect with the temporary sketch plane.",
        )
        self.project_entities = inputs.SelectionByEntityTokenInput(
            id="projectGeometry",
            name="Project Faces/Edges",
            filter=["Faces", "Edges"],
            lower_bound=0,
            upper_bound=0,
            tool_tip="Select faces and edges to project into the temporary sketch.",
        )
        self.heal_tolerance = inputs.FloatInput(
            id="healTolerance",
            name="Heal tolerance",
            default_value=3,
            tool_tip="Maximum endpoint distance for healing projected/intersected curves.",
            units=units,
        )
        self.offset = inputs.FloatInput(
            id="offset",
            name="Offset",
            default_value=0,
            tool_tip="Offset applied to the healed transfer curves.",
            units=units,
        )
        self.operation = inputs.DropDownInput(
            id="operation",
            name="Operation",
            options=[
                TransferShapeInputs.Operations.JOIN,
                TransferShapeInputs.Operations.CUT,
                TransferShapeInputs.Operations.INTERSECT,
            ],
            default_value=TransferShapeInputs.Operations.CUT.value,
            tool_tip="Boolean operation to apply with the generated transfer body.",
        )
        super().__init__()


class TransferShape(custom_compute_feature.CustomComputeFeature):
    inputs: TransferShapeInputs

    @property
    def plugin_name(self) -> str:
        return "Transfer Shape"

    @property
    def plugin_desc(self) -> str:
        return "Transfer intersected/projected shape onto a target body with heal and offset support."

    @property
    def plugin_tooltip(self) -> str:
        return "Transfer intersected/projected shape onto a target body with heal and offset support."

    def get_ui_placement(self) -> ui_placement.UIPlacement:
        section = ui_placement.PlacementSpec(
            id="SeparatorBeforeCustomAddins",
            anchor_id="FusionMoveCommand",
            insert_before=True,
        )
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id=section.id,
            insert_before=True,
        )
        return ui_placement.UIPlacement(
            panel_id="SolidModifyPanel",
            command=command,
            section=section,
        )

    def create_inputs(self) -> TransferShapeInputs:
        return TransferShapeInputs(self.app.activeProduct.unitsManager)

    def execute(self) -> list[combine.Combine]:
        target_face = self.selected_target_face()
        base_sketch = self.selected_base_sketch()
        self.validate_base_sketch(base_sketch, target_face)

        if len(self.inputs.intersect_faces.value) == 0 and len(self.inputs.project_entities.value) == 0:
            raise errors.InvalidInputError("Select at least one intersect face or project geometry entity.")

        component = self.component
        mgr = adsk.fusion.TemporaryBRepManager.get()
        temp_base: adsk.fusion.BaseFeature | None = None
        temp_sketch: adsk.fusion.Sketch | None = None
        try:
            temp_base = component.features.baseFeatures.add()
            temp_base.startEdit()
            component.bRepBodies.add(mgr.copy(target_face.body), temp_base)
            base_body = temp_base.bodies[0]
            base_face = self.find_matching_face(base_body, target_face)
            temp_sketch = component.sketches.addToBaseOrFormFeature(base_face, temp_base, includeFaceEdges=False)

            transfer_curves: list[adsk.fusion.SketchCurve] = []
            transfer_curves.extend(self.intersect_transfer_faces(temp_sketch))
            transfer_curves.extend(self.project_transfer_geometry(temp_sketch, False))
            transfer_curves = self.unique_curves(transfer_curves)

            if not transfer_curves:
                raise errors.InvalidInputError("No transfer curves were created from the selected sources.")

            self.break_curve_links(transfer_curves)
            self.heal_curve_endpoints(transfer_curves)
            # self.apply_offset_to_transfer_curves(temp_sketch, transfer_curves)

            source_sketch_curves = utils.fusion.as_list(base_sketch.sketchCurves)
            if source_sketch_curves:
                temp_sketch.project2(cast(list[adsk.core.Base], source_sketch_curves), True)

            if DEBUG_KEEP_RESULT_SKETCH:
                temp_sketch.name = "Transfer Shape Debug Result"
                if temp_base and temp_base.isValid:
                    temp_base.finishEdit()
                return []

            if temp_sketch.profiles.count < 1:
                raise errors.InvalidInputError(
                    "No closed profile found after transfer. Ensure source geometry can form a closed loop."
                )

            profiles = utils.fusion.as_list(temp_sketch.profiles)
            profiles.sort(key=lambda p: p.areaProperties().area, reverse=True)
            largest_profile = profiles[0]

            target_thickness = utils.brep.get_board_thickness(target_face)
            opposite_face = utils.brep.get_opposite_face(target_face)
            extrude_direction = utils.brep.normal_towards_face(target_face, opposite_face)
            transfer_body = self.create_transfer_body_by_extrude(
                component,
                largest_profile,
                temp_base,
                target_thickness,
                extrude_direction,
            )

            return [combine.Combine(target_face.body, transfer_body, self.selected_operation())]
        finally:
            if temp_base and temp_base.isValid:
                try:
                    temp_base.finishEdit()
                except:
                    pass
                if not DEBUG_KEEP_RESULT_SKETCH:
                    try:
                        temp_base.deleteMe()
                    except:
                        pass

    def selected_target_face(self) -> adsk.fusion.BRepFace:
        selection = cast(list[adsk.fusion.BRepFace], self.inputs.target_face.value)
        if not selection:
            raise errors.InvalidInputError("Select a target face.")
        face = selection[0]
        if not utils.brep.is_planar(face):
            raise errors.InvalidInputError("Target face must be planar.")
        return face

    def selected_base_sketch(self) -> adsk.fusion.Sketch:
        selection = cast(list[adsk.fusion.Sketch], self.inputs.base_sketch.value)
        if not selection:
            raise errors.InvalidInputError("Select a base sketch.")
        return selection[0]

    def validate_base_sketch(self, sketch: adsk.fusion.Sketch, face: adsk.fusion.BRepFace) -> None:
        if sketch.parentComponent != face.body.parentComponent:
            raise errors.InvalidInputError(
                "Base sketch and target face must be in the same component context."
            )
        if not isinstance(face.geometry, adsk.core.Plane):
            raise errors.InvalidInputError("Target face must be planar.")
        sketch_normal = sketch.xDirection.crossProduct(sketch.yDirection)
        sketch_normal.normalize()
        face_normal = face.geometry.normal
        parallel = (
            utils.vector.is_equal_direction(sketch_normal, face_normal)
            or utils.vector.is_opposite_direction(sketch_normal, face_normal)
        )
        if not parallel:
            raise errors.InvalidInputError("Base sketch is not parallel to the target face.")

        distance = abs(face.geometry.normal.dotProduct(face.geometry.origin.vectorTo(sketch.origin)))
        if distance > 1e-6:
            raise errors.InvalidInputError("Base sketch is not on the plane of the target face.")

    def find_matching_face(self, body: adsk.fusion.BRepBody, reference_face: adsk.fusion.BRepFace) -> adsk.fusion.BRepFace:
        if not isinstance(reference_face.geometry, adsk.core.Plane):
            raise errors.InvalidInputError("Target face must be planar.")

        candidates: list[tuple[float, adsk.fusion.BRepFace]] = []
        for face in body.faces:
            if not utils.brep.is_planar(face):
                continue
            if not utils.brep.is_parallel(face, reference_face):
                continue
            if not isinstance(face.geometry, adsk.core.Plane):
                continue
            distance = abs(reference_face.geometry.normal.dotProduct(reference_face.geometry.origin.vectorTo(face.geometry.origin)))
            if distance > 1e-6:
                continue
            area_delta = abs(face.area - reference_face.area)
            candidates.append((area_delta, face))

        if not candidates:
            raise errors.InvalidInputError("Failed to determine target sketch face in temporary base feature.")

        candidates.sort(key=lambda x: x[0])
        return candidates[0][1]

    def create_transfer_body_by_extrude(
        self,
        component: adsk.fusion.Component,
        profile: adsk.fusion.Profile,
        temp_base: adsk.fusion.BaseFeature,
        thickness: float,
        desired_direction: adsk.core.Vector3D,
    ) -> adsk.fusion.BRepBody:
        extrude_input = component.features.extrudeFeatures.createInput(
            profile,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation,  # type: ignore
        )
        extrude_input.targetBaseFeature = temp_base

        sketch = profile.parentSketch
        sketch_normal = sketch.xDirection.crossProduct(sketch.yDirection)
        sketch_normal.normalize()
        direction = (
            adsk.fusion.ExtentDirections.PositiveExtentDirection
            if sketch_normal.dotProduct(desired_direction) >= 0
            else adsk.fusion.ExtentDirections.NegativeExtentDirection
        )
        extent = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(thickness))
        extrude_input.setOneSideExtent(extent, direction)  # type: ignore

        extrude_feature = component.features.extrudeFeatures.add(extrude_input)
        if extrude_feature.bodies.count < 1:
            raise errors.InvalidInputError("Failed to create transfer body from profile extrusion.")

        mgr = adsk.fusion.TemporaryBRepManager.get()
        return mgr.copy(extrude_feature.bodies[0])

    def intersect_transfer_faces(self, sketch: adsk.fusion.Sketch) -> list[adsk.fusion.SketchCurve]:
        selected_faces = cast(list[adsk.fusion.BRepFace], self.inputs.intersect_faces.value)
        if not selected_faces:
            return []
        created = sketch.intersectWithSketchPlane(cast(list[adsk.core.Base], selected_faces))
        intersected_curves = self.extract_sketch_curves(created)
        if not intersected_curves:
            return []

        # Intersected curves can remain linked even when re-projected.
        # Recreate them explicitly from transient geometry to guarantee
        # unlinked editable sketch curves.
        recreated = self.recreate_curves_from_geometry(sketch, intersected_curves)
        for curve in intersected_curves:
            try:
                if curve.isValid and curve.isDeletable:
                    curve.deleteMe()
            except:
                pass
        return recreated if recreated else intersected_curves

    def project_transfer_geometry(self, sketch: adsk.fusion.Sketch, linked: bool) -> list[adsk.fusion.SketchCurve]:
        entities = cast(list[adsk.fusion.BRepFace | adsk.fusion.BRepEdge], self.inputs.project_entities.value)
        if not entities:
            return []
        created = sketch.project2(cast(list[adsk.core.Base], entities), linked)
        return self.extract_sketch_curves(created)

    def extract_sketch_curves(self, entities: list[adsk.fusion.SketchEntity]) -> list[adsk.fusion.SketchCurve]:
        result: list[adsk.fusion.SketchCurve] = []
        for entity in entities:
            curve = adsk.fusion.SketchCurve.cast(entity)
            if curve:
                result.append(curve)
        return result

    def unique_curves(self, curves: list[adsk.fusion.SketchCurve]) -> list[adsk.fusion.SketchCurve]:
        result: list[adsk.fusion.SketchCurve] = []
        seen: set[str] = set()
        for curve in curves:
            token = curve.entityToken
            if token in seen:
                continue
            seen.add(token)
            result.append(curve)
        return result

    def recreate_curves_from_geometry(
        self, sketch: adsk.fusion.Sketch, source_curves: list[adsk.fusion.SketchCurve]
    ) -> list[adsk.fusion.SketchCurve]:
        recreated: list[adsk.fusion.SketchCurve] = []
        for curve in source_curves:
            line = adsk.fusion.SketchLine.cast(curve)
            if line:
                start = line.startSketchPoint.geometry
                end = line.endSketchPoint.geometry
                new_line = sketch.sketchCurves.sketchLines.addByTwoPoints(start, end)
                if new_line:
                    recreated.append(new_line)
                continue

            nurbs = curve.geometry if isinstance(curve.geometry, adsk.core.NurbsCurve3D) else curve.geometry.asNurbsCurve  # type: ignore
            points = self.sample_fit_points_from_nurbs(nurbs)
            if len(points) < 2:
                continue
            fit_points = adsk.core.ObjectCollection.create()
            for point in points:
                fit_points.add(point)
            spline = sketch.sketchCurves.sketchFittedSplines.add(fit_points)
            if spline:
                recreated.append(spline)
        return recreated

    def sample_fit_points_from_nurbs(self, curve: adsk.core.NurbsCurve3D) -> list[adsk.core.Point3D]:
        evaluator = curve.evaluator
        ok, start_param, end_param = evaluator.getParameterExtents()
        if not ok:
            return []
        ok, total_length = evaluator.getLengthAtParameter(start_param, end_param)
        if not ok:
            return []

        spacing = max(0.1, utils.sketch.nurbs_length(curve) / 20) 
        points: list[adsk.core.Point3D] = []
        ok, start_point = evaluator.getPointAtParameter(start_param)
        if ok:
            points.append(start_point)
        offset = spacing
        while offset < total_length:
            ok, param = evaluator.getParameterAtLength(start_param, offset)
            if not ok:
                break
            ok, point = evaluator.getPointAtParameter(param)
            if not ok:
                break
            points.append(point)
            offset += spacing
        ok, end_point = evaluator.getPointAtParameter(end_param)
        if ok:
            points.append(end_point)
        return points

    def break_curve_links(self, curves: list[adsk.fusion.SketchCurve]) -> None:
        for curve in curves:
            try:
                if curve.isReference:
                    curve.isReference = False
            except:
                pass

    def heal_curve_endpoints(self, curves: list[adsk.fusion.SketchCurve]) -> None:
        tolerance = self.inputs.heal_tolerance.value
        if tolerance <= 0:
            return

        if len(curves) == 0:
            return

        sketch = curves[0].parentSketch
        epsilon = 1e-9

        class OpenChain:
            def __init__(self, start: adsk.fusion.SketchPoint, end: adsk.fusion.SketchPoint):
                self.start = start
                self.end = end

        def point_distance(p1: adsk.fusion.SketchPoint, p2: adsk.fusion.SketchPoint) -> float:
            return p1.geometry.distanceTo(p2.geometry)

        def is_same_point(p1: adsk.fusion.SketchPoint, p2: adsk.fusion.SketchPoint) -> bool:
            return point_distance(p1, p2) <= epsilon

        def append_or_merge_segment(
            chains: list[OpenChain], p_start: adsk.fusion.SketchPoint, p_end: adsk.fusion.SketchPoint
        ) -> None:
            matches_start: list[tuple[float, int, str]] = []
            matches_end: list[tuple[float, int, str]] = []
            for idx, chain in enumerate(chains):
                dist = point_distance(p_start, chain.start)
                if dist <= epsilon:
                    matches_start.append((dist, idx, "start"))
                dist = point_distance(p_start, chain.end)
                if dist <= epsilon:
                    matches_start.append((dist, idx, "end"))
                dist = point_distance(p_end, chain.start)
                if dist <= epsilon:
                    matches_end.append((dist, idx, "start"))
                dist = point_distance(p_end, chain.end)
                if dist <= epsilon:
                    matches_end.append((dist, idx, "end"))

            match_start = min(matches_start, default=None, key=lambda x: x[0])
            match_end = min(matches_end, default=None, key=lambda x: x[0])

            if not match_start and not match_end:
                chains.append(OpenChain(p_start, p_end))
                return

            if match_start and not match_end:
                _, idx, side = match_start
                if side == "start":
                    chains[idx].start = p_end
                else:
                    chains[idx].end = p_end
                return

            if match_end and not match_start:
                _, idx, side = match_end
                if side == "start":
                    chains[idx].start = p_start
                else:
                    chains[idx].end = p_start
                return

            _, idx_start, side_start = match_start
            _, idx_end, side_end = match_end

            if idx_start == idx_end:
                if side_start != side_end:
                    chains.pop(idx_start)
                return

            chain_a = chains[idx_start]
            chain_b = chains[idx_end]
            free_a = chain_a.end if side_start == "start" else chain_a.start
            free_b = chain_b.end if side_end == "start" else chain_b.start

            for remove_idx in sorted([idx_start, idx_end], reverse=True):
                chains.pop(remove_idx)

            if not is_same_point(free_a, free_b):
                chains.append(OpenChain(free_a, free_b))

        def collapse_touching_chains(chains: list[OpenChain]) -> None:
            changed = True
            while changed:
                changed = False
                for i in range(len(chains)):
                    if changed:
                        break
                    for j in range(i + 1, len(chains)):
                        candidates = [
                            (point_distance(chains[i].start, chains[j].start), "start", "start"),
                            (point_distance(chains[i].start, chains[j].end), "start", "end"),
                            (point_distance(chains[i].end, chains[j].start), "end", "start"),
                            (point_distance(chains[i].end, chains[j].end), "end", "end"),
                        ]
                        candidates.sort(key=lambda x: x[0])
                        dist, side_i, side_j = candidates[0]
                        if dist > epsilon:
                            continue

                        free_i = chains[i].end if side_i == "start" else chains[i].start
                        free_j = chains[j].end if side_j == "start" else chains[j].start

                        for remove_idx in sorted([i, j], reverse=True):
                            chains.pop(remove_idx)
                        if not is_same_point(free_i, free_j):
                            chains.append(OpenChain(free_i, free_j))
                        changed = True
                        break

        open_chains: list[OpenChain] = []
        for curve in curves:
            start_point = adsk.fusion.SketchPoint.cast(getattr(curve, "startSketchPoint", None))
            end_point = adsk.fusion.SketchPoint.cast(getattr(curve, "endSketchPoint", None))
            if not start_point or not end_point:
                continue
            append_or_merge_segment(open_chains, start_point, end_point)

        if len(open_chains) < 2:
            return

        while True:
            collapse_touching_chains(open_chains)
            if len(open_chains) == 1:
                chain = open_chains[0]
                if chain.start.isValid and chain.end.isValid:
                    closing_dist = point_distance(chain.start, chain.end)
                    if epsilon < closing_dist <= tolerance:
                        try:
                            line = sketch.sketchCurves.sketchLines.addByTwoPoints(chain.start, chain.end)
                            if line:
                                open_chains.pop()
                        except Exception as error:
                            utils.fusion.log(f"Failed to close final open chain: {error}")
                break

            if len(open_chains) < 2:
                break

            candidate_pairs: list[tuple[float, int, str, int, str]] = []
            for i in range(len(open_chains)):
                for j in range(i + 1, len(open_chains)):
                    combinations = [
                        (point_distance(open_chains[i].start, open_chains[j].start), "start", "start"),
                        (point_distance(open_chains[i].start, open_chains[j].end), "start", "end"),
                        (point_distance(open_chains[i].end, open_chains[j].start), "end", "start"),
                        (point_distance(open_chains[i].end, open_chains[j].end), "end", "end"),
                    ]
                    for dist, side_i, side_j in combinations:
                        if dist <= epsilon or dist > tolerance:
                            continue
                        candidate_pairs.append((dist, i, side_i, j, side_j))

            if not candidate_pairs:
                break

            candidate_pairs.sort(key=lambda x: x[0])
            _, idx_a, side_a, idx_b, side_b = candidate_pairs[0]
            chain_a = open_chains[idx_a]
            chain_b = open_chains[idx_b]
            point_a = chain_a.start if side_a == "start" else chain_a.end
            point_b = chain_b.start if side_b == "start" else chain_b.end

            if not point_a.isValid or not point_b.isValid or point_a == point_b:
                break

            try:
                line = sketch.sketchCurves.sketchLines.addByTwoPoints(point_a, point_b)
                if not line:
                    raise RuntimeError("Failed to create healing line.")
            except Exception as error:
                utils.fusion.log(f"Failed to create healing line between points: {error}")
                break

            free_a = chain_a.end if side_a == "start" else chain_a.start
            free_b = chain_b.end if side_b == "start" else chain_b.start
            for remove_idx in sorted([idx_a, idx_b], reverse=True):
                open_chains.pop(remove_idx)
            if not is_same_point(free_a, free_b):
                open_chains.append(OpenChain(free_a, free_b))

    class EndpointNode:
        def __init__(self, point: adsk.fusion.SketchPoint):
            self.point = point
            self.curve_ids: set[str] = set()
            self.point_tokens: set[str] = set()

    def sketch_point_token(self, point: adsk.fusion.SketchPoint) -> str:
        native = adsk.fusion.SketchPoint.cast(point.nativeObject) or point
        return native.entityToken

    def build_endpoint_nodes(self, curves: list[adsk.fusion.SketchCurve]) -> dict[str, EndpointNode]:
        nodes_by_token: dict[str, TransferShape.EndpointNode] = {}

        for curve in curves:
            cid = curve.entityToken
            start_point = adsk.fusion.SketchPoint.cast(getattr(curve, "startSketchPoint", None))
            end_point = adsk.fusion.SketchPoint.cast(getattr(curve, "endSketchPoint", None))
            for point in [start_point, end_point]:
                if not point:
                    continue
                pid = self.sketch_point_token(point)
                if pid not in nodes_by_token:
                    nodes_by_token[pid] = TransferShape.EndpointNode(point)
                    nodes_by_token[pid].point_tokens.add(pid)
                nodes_by_token[pid].curve_ids.add(cid)

        # Merge geometrically coincident endpoints so they don't appear as
        # separate open nodes and attract unrelated connections.
        merged_nodes: list[TransferShape.EndpointNode] = []
        for node in nodes_by_token.values():
            merged_into_existing = False
            for existing in merged_nodes:
                if existing.point.geometry.distanceTo(node.point.geometry) <= 1e-9:
                    existing.curve_ids.update(node.curve_ids)
                    existing.point_tokens.update(node.point_tokens)
                    merged_into_existing = True
                    break
            if not merged_into_existing:
                merged_nodes.append(node)

        return {str(idx): node for idx, node in enumerate(merged_nodes)}

    def apply_offset_to_transfer_curves(self, sketch: adsk.fusion.Sketch, curves: list[adsk.fusion.SketchCurve]) -> None:
        offset = self.inputs.offset.value
        if abs(offset) <= 1e-9:
            return
        try:
            offset_input = sketch.geometricConstraints.createOffsetInput(
                curves,
                adsk.core.ValueInput.createByReal(offset),
            )
            offset_input.isTopologyMatched = False
            constraint = sketch.geometricConstraints.addOffset2(offset_input)
            if not constraint or len(constraint.childCurves) == 0:
                raise errors.InvalidInputError("Offset did not produce any curves.")
            sketch.setConstructionState(curves, adsk.fusion.SketchCurveConstructionStates.ConstructionSketchCurveConstructionState)  # type: ignore
        except errors.InvalidInputError:
            raise
        except Exception as error:
            raise errors.InvalidInputError(f"Offset failed: {error}")

    def selected_operation(self) -> combine.Operation:
        value = self.inputs.operation.value
        if value == TransferShapeInputs.Operations.JOIN.value:
            return combine.Operation.JOIN
        if value == TransferShapeInputs.Operations.CUT.value:
            return combine.Operation.CUT
        if value == TransferShapeInputs.Operations.INTERSECT.value:
            return combine.Operation.INTERSECT
        raise errors.InvalidInputError("Unsupported combine operation selected.")

    def pre_select(self, input, selection) -> bool:
        if input.id == self.inputs.target_face.id:
            return isinstance(selection, adsk.fusion.BRepFace) and utils.brep.is_planar(selection)
        if input.id == self.inputs.base_sketch.id:
            if not isinstance(selection, adsk.fusion.Sketch):
                return False
            target = cast(list[adsk.fusion.BRepFace], self.inputs.target_face.value)
            if not target:
                return True
            face = target[0]
            try:
                self.validate_base_sketch(selection, face)
                return True
            except:
                return False
        if input.id == self.inputs.intersect_faces.id:
            return isinstance(selection, adsk.fusion.BRepFace)
        if input.id == self.inputs.project_entities.id:
            return isinstance(selection, adsk.fusion.BRepFace) or isinstance(selection, adsk.fusion.BRepEdge)
        return True
