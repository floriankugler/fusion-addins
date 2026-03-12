from lib import custom_compute_feature, inputs, combine, errors, utils, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from typing import cast
from dataclasses import dataclass

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
            lower_bound=0,
            upper_bound=1,
            tool_tip="Optional: select a sketch to project into the transfer sketch.",
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
            name="Project Edges",
            filter=["Edges"],
            lower_bound=0,
            upper_bound=0,
            tool_tip="Select edges to project into the temporary sketch.",
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

        if len(self.inputs.intersect_faces.value) == 0 and len(self.inputs.project_entities.value) == 0:
            raise errors.InvalidInputError("Select at least one intersect face or project geometry entity.")

        component = self.component
        mgr = adsk.fusion.TemporaryBRepManager.get()
        temp_base: adsk.fusion.BaseFeature
        try:
            temp_base = component.features.baseFeatures.add()
            temp_base.startEdit()
            component.bRepBodies.add(mgr.copy(target_face.body), temp_base)
            base_body = temp_base.bodies[0]
            base_face = self.find_matching_face(base_body, target_face)
            temp_sketch = component.sketches.addToBaseOrFormFeature(base_face, temp_base, includeFaceEdges=False)

            source_curves: list[adsk.fusion.SketchCurve] = []
            source_curves.extend(self.intersect_transfer_faces(temp_sketch))
            source_curves.extend(self.project_transfer_geometry(temp_sketch, False))
            source_curves = self.unique_curves(source_curves)

            if not source_curves:
                raise errors.InvalidInputError("No transfer curves were created from the selected sources.")

            self.break_curve_links(source_curves)
            rebuilt = self.rebuild_intersection_chains_as_splines(temp_sketch, source_curves)
            if rebuilt:
                for curve in source_curves:
                    try:
                        if curve.isValid and curve.isDeletable:
                            curve.deleteMe()
                    except:
                        pass
                transfer_curves = rebuilt
            else:
                transfer_curves = source_curves

            transfer_curves = self.apply_offset_to_transfer_curves(temp_sketch, transfer_curves)

            if base_sketch:
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

    def selected_base_sketch(self) -> adsk.fusion.Sketch | None:
        selection = cast(list[adsk.fusion.Sketch], self.inputs.base_sketch.value)
        if not selection:
            return None
        return selection[0]

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
        return intersected_curves

    def project_transfer_geometry(self, sketch: adsk.fusion.Sketch, linked: bool) -> list[adsk.fusion.SketchCurve]:
        entities = cast(list[adsk.fusion.BRepEdge], self.inputs.project_entities.value)
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

    def rebuild_intersection_chains_as_splines(
        self, sketch: adsk.fusion.Sketch, curves: list[adsk.fusion.SketchCurve]
    ) -> list[adsk.fusion.SketchCurve]:
        if len(curves) < 2:
            return []

        connection_tolerance = max(self.inputs.heal_tolerance.value, 1e-6)
        ordered_groups = self.order_curve_groups_by_endpoint_proximity(curves, connection_tolerance)
        if len(ordered_groups) == 0:
            return []

        sample_spacing = 0.35  # 3.5 mm in Fusion internal units (cm).
        min_fit_point_spacing = 0.3  # 3 mm minimum spacing between fit points.
        splines: list[adsk.fusion.SketchCurve] = []
        for ordered in ordered_groups:
            sampled_points: list[adsk.core.Point3D] = []
            for curve, reverse in ordered:
                points = self.sample_curve_points(curve, sample_spacing, reverse)
                for point in points:
                    if sampled_points and sampled_points[-1].distanceTo(point) < min_fit_point_spacing:
                        continue
                    sampled_points.append(point)

            if len(sampled_points) < 2:
                continue

            spline: adsk.fusion.SketchCurve | None = None
            try:
                # Degree-5 control-point spline provides C2 continuity.
                if len(sampled_points) >= 6:
                    spline = sketch.sketchCurves.sketchControlPointSplines.add(
                        cast(list[adsk.core.Base], sampled_points),
                        adsk.fusion.SplineDegrees.SplineDegreeFive,
                    )
                elif len(sampled_points) >= 4:
                    spline = sketch.sketchCurves.sketchControlPointSplines.add(
                        cast(list[adsk.core.Base], sampled_points),
                        adsk.fusion.SplineDegrees.SplineDegreeThree,
                    )
            except:
                spline = None

            if not spline:
                fit_points = adsk.core.ObjectCollection.create()
                for point in sampled_points:
                    fit_points.add(point)
                spline = sketch.sketchCurves.sketchFittedSplines.add(fit_points)

            if spline:
                splines.append(spline)

        return splines

    def order_curve_groups_by_endpoint_proximity(
        self, curves: list[adsk.fusion.SketchCurve], tolerance: float
    ) -> list[list[tuple[adsk.fusion.SketchCurve, bool]]]:
        if len(curves) == 0:
            return []

        def endpoints(curve: adsk.fusion.SketchCurve) -> tuple[adsk.fusion.SketchPoint | None, adsk.fusion.SketchPoint | None]:
            return (
                adsk.fusion.SketchPoint.cast(getattr(curve, "startSketchPoint", None)),
                adsk.fusion.SketchPoint.cast(getattr(curve, "endSketchPoint", None)),
            )
        valid_indices = [i for i in range(len(curves)) if all(endpoints(curves[i]))]
        if not valid_indices:
            return []

        def best_attachment(
            end_point: adsk.fusion.SketchPoint, candidates: set[int]
        ) -> tuple[float, int, bool, adsk.fusion.SketchPoint] | None:
            best: tuple[float, int, bool, adsk.fusion.SketchPoint] | None = None
            for idx in candidates:
                s, e = endpoints(curves[idx])
                if not s or not e:
                    continue
                ds = end_point.geometry.distanceTo(s.geometry)
                if ds <= tolerance:
                    candidate = (ds, idx, False, e)
                    if best is None or candidate[0] < best[0]:
                        best = candidate
                de = end_point.geometry.distanceTo(e.geometry)
                if de <= tolerance:
                    candidate = (de, idx, True, s)
                    if best is None or candidate[0] < best[0]:
                        best = candidate
            return best

        def are_curves_connected(i: int, j: int) -> bool:
            si, ei = endpoints(curves[i])
            sj, ej = endpoints(curves[j])
            if not si or not ei or not sj or not ej:
                return False
            return (
                si.geometry.distanceTo(sj.geometry) <= tolerance
                or si.geometry.distanceTo(ej.geometry) <= tolerance
                or ei.geometry.distanceTo(sj.geometry) <= tolerance
                or ei.geometry.distanceTo(ej.geometry) <= tolerance
            )

        # Build connected components first, so curves within healing distance
        # are handled in a single group and don't split into separate splines.
        adjacency: dict[int, set[int]] = {idx: set() for idx in valid_indices}
        for i_pos in range(len(valid_indices)):
            i = valid_indices[i_pos]
            for j_pos in range(i_pos + 1, len(valid_indices)):
                j = valid_indices[j_pos]
                if are_curves_connected(i, j):
                    adjacency[i].add(j)
                    adjacency[j].add(i)

        components: list[set[int]] = []
        unvisited = set(valid_indices)
        while unvisited:
            seed = next(iter(unvisited))
            stack = [seed]
            component: set[int] = set()
            while stack:
                current = stack.pop()
                if current in component:
                    continue
                component.add(current)
                for neighbor in adjacency[current]:
                    if neighbor not in component:
                        stack.append(neighbor)
            components.append(component)
            unvisited -= component

        ordered_groups: list[list[tuple[adsk.fusion.SketchCurve, bool]]] = []

        for component in components:
            remaining = set(component)
            seed_idx = next(iter(remaining))
            s0, e0 = endpoints(curves[seed_idx])
            if not s0 or not e0:
                continue

            ordered: list[tuple[adsk.fusion.SketchCurve, bool]] = [(curves[seed_idx], False)]
            remaining.remove(seed_idx)
            head = s0
            tail = e0

            while True:
                tail_candidate = best_attachment(tail, remaining)
                head_candidate = best_attachment(head, remaining)

                chosen_end: str | None = None
                chosen: tuple[float, int, bool, adsk.fusion.SketchPoint] | None = None
                if tail_candidate and head_candidate:
                    if tail_candidate[0] <= head_candidate[0]:
                        chosen_end = "tail"
                        chosen = tail_candidate
                    else:
                        chosen_end = "head"
                        chosen = head_candidate
                elif tail_candidate:
                    chosen_end = "tail"
                    chosen = tail_candidate
                elif head_candidate:
                    chosen_end = "head"
                    chosen = head_candidate
                else:
                    break

                _, idx, reverse, next_point = chosen
                remaining.remove(idx)
                if chosen_end == "tail":
                    ordered.append((curves[idx], reverse))
                    tail = next_point
                else:
                    ordered.insert(0, (curves[idx], not reverse))
                    head = next_point

            # If ordering stalls due to branching ambiguity, keep remaining
            # curves in this same component/group instead of creating a new group.
            while remaining:
                idx = remaining.pop()
                ordered.append((curves[idx], False))

            ordered_groups.append(ordered)

        return ordered_groups

    def sample_curve_points(
        self, curve: adsk.fusion.SketchCurve, spacing: float, reverse: bool
    ) -> list[adsk.core.Point3D]:
        geometry = curve.geometry
        nurbs = geometry if isinstance(geometry, adsk.core.NurbsCurve3D) else geometry.asNurbsCurve  # type: ignore
        evaluator = nurbs.evaluator

        ok, start_param, end_param = evaluator.getParameterExtents()
        if not ok:
            return []
        ok, total_length = evaluator.getLengthAtParameter(start_param, end_param)
        if not ok:
            return []

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

        if reverse:
            points.reverse()
        return points

    def break_curve_links(self, curves: list[adsk.fusion.SketchCurve]) -> None:
        for curve in curves:
            try:
                if curve.isReference:
                    curve.isReference = False
            except:
                pass

    @dataclass
    class OpenChain:
        start: adsk.fusion.SketchPoint
        end: adsk.fusion.SketchPoint

    def sketch_point_token(self, point: adsk.fusion.SketchPoint) -> str:
        native = adsk.fusion.SketchPoint.cast(point.nativeObject) or point
        return native.entityToken

    def point_distance(self, p1: adsk.fusion.SketchPoint, p2: adsk.fusion.SketchPoint) -> float:
        return p1.geometry.distanceTo(p2.geometry)

    def is_same_point(self, p1: adsk.fusion.SketchPoint, p2: adsk.fusion.SketchPoint, epsilon: float = 1e-9) -> bool:
        return self.point_distance(p1, p2) <= epsilon

    def append_or_merge_segment(
        self,
        chains: list["TransferShape.OpenChain"],
        p_start: adsk.fusion.SketchPoint,
        p_end: adsk.fusion.SketchPoint,
    ) -> None:
        start_token = self.sketch_point_token(p_start)
        end_token = self.sketch_point_token(p_end)
        matches_start: list[tuple[float, int, str]] = []
        matches_end: list[tuple[float, int, str]] = []
        for idx, chain in enumerate(chains):
            chain_start_token = self.sketch_point_token(chain.start)
            chain_end_token = self.sketch_point_token(chain.end)
            if start_token == chain_start_token:
                matches_start.append((0.0, idx, "start"))
            if start_token == chain_end_token:
                matches_start.append((0.0, idx, "end"))
            if end_token == chain_start_token:
                matches_end.append((0.0, idx, "start"))
            if end_token == chain_end_token:
                matches_end.append((0.0, idx, "end"))

        match_start = min(matches_start, default=None, key=lambda x: x[0])
        match_end = min(matches_end, default=None, key=lambda x: x[0])

        if not match_start and not match_end:
            chains.append(TransferShape.OpenChain(p_start, p_end))
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

        if self.sketch_point_token(free_a) != self.sketch_point_token(free_b):
            chains.append(TransferShape.OpenChain(free_a, free_b))

    def merge_one_touching_chain_pair(self, chains: list["TransferShape.OpenChain"]) -> bool:
        for i in range(len(chains)):
            for j in range(i + 1, len(chains)):
                combinations = [
                    (self.sketch_point_token(chains[i].start) == self.sketch_point_token(chains[j].start), "start", "start"),
                    (self.sketch_point_token(chains[i].start) == self.sketch_point_token(chains[j].end), "start", "end"),
                    (self.sketch_point_token(chains[i].end) == self.sketch_point_token(chains[j].start), "end", "start"),
                    (self.sketch_point_token(chains[i].end) == self.sketch_point_token(chains[j].end), "end", "end"),
                ]
                match = next((match for match in combinations if match[0]), None)
                if not match:
                    continue
                _, side_i, side_j = match

                free_i = chains[i].end if side_i == "start" else chains[i].start
                free_j = chains[j].end if side_j == "start" else chains[j].start

                for remove_idx in sorted([i, j], reverse=True):
                    chains.pop(remove_idx)
                if self.sketch_point_token(free_i) != self.sketch_point_token(free_j):
                    chains.append(TransferShape.OpenChain(free_i, free_j))
                return True
        return False

    def best_patch_candidate(
        self, chains: list["TransferShape.OpenChain"], tolerance: float
    ) -> tuple[int, str, int, str] | None:
        best: tuple[float, int, str, int, str] | None = None
        for i in range(len(chains)):
            for j in range(i + 1, len(chains)):
                combinations = [
                    (self.point_distance(chains[i].start, chains[j].start), "start", "start"),
                    (self.point_distance(chains[i].start, chains[j].end), "start", "end"),
                    (self.point_distance(chains[i].end, chains[j].start), "end", "start"),
                    (self.point_distance(chains[i].end, chains[j].end), "end", "end"),
                ]
                for dist, side_i, side_j in combinations:
                    if dist > tolerance:
                        continue
                    if best is None or dist < best[0]:
                        best = (dist, i, side_i, j, side_j)
        if best is None:
            return None
        _, i, side_i, j, side_j = best
        return i, side_i, j, side_j

    def connect_chain_endpoints(
        self,
        sketch: adsk.fusion.Sketch,
        point_a: adsk.fusion.SketchPoint,
        point_b: adsk.fusion.SketchPoint,
        delta: float,
        coincident_threshold: float,
    ) -> tuple[bool, adsk.fusion.SketchCurve | None]:
        if delta < coincident_threshold:
            try:
                constraint = sketch.geometricConstraints.addCoincident(point_a, point_b)
                if constraint:
                    return True, None
            except:
                pass

        line = sketch.sketchCurves.sketchLines.addByTwoPoints(point_a, point_b)
        if line:
            return True, line
        return False, None

    def heal_curve_endpoints(self, curves: list[adsk.fusion.SketchCurve]) -> list[adsk.fusion.SketchCurve]:
        tolerance = self.inputs.heal_tolerance.value
        if tolerance <= 0:
            return []

        if len(curves) == 0:
            return []

        sketch = curves[0].parentSketch
        coincident_threshold = 0.1  # 1 mm in Fusion internal units (cm).
        patch_curves: list[adsk.fusion.SketchCurve] = []

        open_chains: list[TransferShape.OpenChain] = []
        for curve in curves:
            start_point = adsk.fusion.SketchPoint.cast(getattr(curve, "startSketchPoint", None))
            end_point = adsk.fusion.SketchPoint.cast(getattr(curve, "endSketchPoint", None))
            if not start_point or not end_point:
                continue
            self.append_or_merge_segment(open_chains, start_point, end_point)

        if len(open_chains) < 2:
            return []

        while True:
            while self.merge_one_touching_chain_pair(open_chains):
                pass

            if len(open_chains) == 1:
                chain = open_chains[0]
                try:
                    if self.sketch_point_token(chain.start) == self.sketch_point_token(chain.end):
                        open_chains.pop()
                        break

                    delta = self.point_distance(chain.start, chain.end)
                    if delta <= tolerance:
                        success, created_curve = self.connect_chain_endpoints(
                            sketch, chain.start, chain.end, delta, coincident_threshold
                        )
                        if success:
                            if created_curve:
                                patch_curves.append(created_curve)
                            open_chains.pop()
                            break
                    else:
                        open_chains.pop()
                except Exception as error:
                    utils.fusion.log(f"Failed to close final open chain: {error}")
                break

            if len(open_chains) < 2:
                break

            candidate = self.best_patch_candidate(open_chains, tolerance)
            if candidate is None:
                break

            idx_a, side_a, idx_b, side_b = candidate
            chain_a = open_chains[idx_a]
            chain_b = open_chains[idx_b]
            point_a = chain_a.start if side_a == "start" else chain_a.end
            point_b = chain_b.start if side_b == "start" else chain_b.end

            if not point_a.isValid or not point_b.isValid or point_a == point_b:
                break

            try:
                delta = self.point_distance(point_a, point_b)
                success, created_curve = self.connect_chain_endpoints(
                    sketch, point_a, point_b, delta, coincident_threshold
                )
                if not success:
                    raise RuntimeError("Failed to create healing line.")
                if created_curve:
                    patch_curves.append(created_curve)
            except Exception as error:
                utils.fusion.log(f"Failed to create healing line between points: {error}")
                break

            free_a = chain_a.end if side_a == "start" else chain_a.start
            free_b = chain_b.end if side_b == "start" else chain_b.start
            for remove_idx in sorted([idx_a, idx_b], reverse=True):
                open_chains.pop(remove_idx)
            if self.sketch_point_token(free_a) != self.sketch_point_token(free_b):
                open_chains.append(TransferShape.OpenChain(free_a, free_b))

        return patch_curves

    def apply_offset_to_transfer_curves(
        self, sketch: adsk.fusion.Sketch, curves: list[adsk.fusion.SketchCurve]
    ) -> list[adsk.fusion.SketchCurve]:
        offset = self.inputs.offset.value
        if abs(offset) <= 1e-9:
            return curves
        try:
            offset_input = sketch.geometricConstraints.createOffsetInput(
                curves,
                adsk.core.ValueInput.createByReal(offset),
            )
            offset_input.isTopologyMatched = False
            constraint = sketch.geometricConstraints.addOffset2(offset_input)
            if not constraint:
                raise errors.InvalidInputError("Offset did not produce any curves.")
            offset_curves = self.extract_sketch_curves(self.vector_to_list(constraint.childCurves))
            if len(offset_curves) == 0:
                raise errors.InvalidInputError("Offset did not produce any curves.")
            sketch.setConstructionState(curves, adsk.fusion.SketchCurveConstructionStates.ConstructionSketchCurveConstructionState)  # type: ignore
            if not offset_curves:
                raise errors.InvalidInputError("Offset did not return sketch curves.")

            rebuilt_curves = self.rebuild_intersection_chains_as_splines(sketch, offset_curves)
            if rebuilt_curves:
                for curve in offset_curves:
                    try:
                        if curve.isValid and curve.isDeletable:
                            curve.deleteMe()
                    except:
                        pass
                return rebuilt_curves
            return offset_curves
        except errors.InvalidInputError:
            raise
        except Exception as error:
            raise errors.InvalidInputError(f"Offset failed: {error}")

    def vector_to_list(self, values) -> list:
        try:
            return [values.item(i) for i in range(values.count)]
        except:
            pass
        try:
            return [item for item in values]
        except:
            return []

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
            return isinstance(selection, adsk.fusion.Sketch)
        if input.id == self.inputs.intersect_faces.id:
            return isinstance(selection, adsk.fusion.BRepFace)
        if input.id == self.inputs.project_entities.id:
            return isinstance(selection, adsk.fusion.BRepEdge)
        return True
