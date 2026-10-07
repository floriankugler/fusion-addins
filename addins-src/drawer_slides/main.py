import os
from dataclasses import dataclass
from typing import cast

import adsk.core
import adsk.fusion

from lib import (
    addin,
    drawer_slides,
    edge_sketch,
    hole_features,
    inputs,
    ui_placement,
    utils,
)
from lib.fusionbootstrap.runtime import RuntimeInfo


_addin: addin.Addin | None = None

NAME = "Drawer Slides"
#: Centimeters (Fusion's internal length unit) per millimeter.
MM = 0.1
#: Two positions closer than this (cm) count as the same.
SAME_POSITION = 1e-4


def _mm(value_cm: float) -> str:
    return f"{value_cm * 10:.6g} mm"


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = DrawerSlides(runtime_info)
    # Dev support: allow external tooling to restart this add-in by firing the
    # custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "drawer_slides.py",
    )
    reloader.ensure(runtime_info.id + "_reload", entry)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class DrawerSlidesInputs(inputs.Inputs):
    class HoleSets:
        ODD = inputs.DropDownInput.Item("Odd", 0)
        EVEN = inputs.DropDownInput.Item("Even", 1)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        Item = inputs.DropDownInput.Item
        self.front_edges = inputs.SelectionByEntityTokenInput(
            id="front_edges",
            name="Front Edges",
            filter=["LinearEdges"],
            lower_bound=1,
            upper_bound=0,
            tool_tip=(
                "Select the front edge of each carcass side, on the face the "
                "slide is screwed to. The holes are laid out on the first "
                "side and projected onto the others."
            ),
        )
        self.heights = inputs.SelectionByEntityTokenInput(
            id="slide_heights",
            name="Slide Heights",
            filter=[
                "LinearEdges",
                "SketchLines",
                "Vertices",
                "SketchPoints",
                "ConstructionPoints",
            ],
            lower_bound=1,
            upper_bound=0,
            tool_tip=(
                "Select one horizontal edge, sketch line or point per slide, "
                "at the height its runner rests on (e.g. the top of the "
                "carcass bottom)."
            ),
        )
        self.slide_type = inputs.DropDownInput(
            id="slide_type",
            name="Slide",
            options=[
                Item(model.name, model.value)
                for model in drawer_slides.SLIDE_MODELS
            ],
            default_value=drawer_slides.MOVENTO_760H.value,
            tool_tip="The drawer slide whose cabinet holes are drilled.",
        )
        # One length dropdown per slide model, since each model comes in
        # different lengths; only the selected model's dropdown is shown.
        for model in drawer_slides.SLIDE_MODELS:
            lengths = model.nominal_lengths
            setattr(
                self,
                self.nominal_length_id(model),
                inputs.DropDownInput(
                    id=self.nominal_length_id(model),
                    name="Nominal Length",
                    options=[Item(f"{length} mm", length) for length in lengths],
                    default_value=500 if 500 in lengths else lengths[0],
                    tool_tip=(
                        "The slide's nominal length (NL). The cabinet must be "
                        "at least NL + 3 mm deep."
                    ),
                    update_visibility=(
                        lambda model=model: self.slide_type.value == model.value
                    ),
                ),
            )
        self.holes_per_slide = inputs.IntegerInput(
            id="holes_per_slide",
            name="Holes per Slide",
            default_value=4,
            minimum=2,
            maximum=12,
            tool_tip=(
                "Number of pre-drill holes per slide, spread evenly over the "
                "holes the runner offers."
            ),
        )
        self.hole_set = inputs.DropDownInput(
            id="hole_set",
            name="Hole Set",
            options=utils.misc.class_property_values(
                DrawerSlidesInputs.HoleSets,
                inputs.DropDownInput.Item,
            ),
            default_value=DrawerSlidesInputs.HoleSets.ODD.value,
            tool_tip=(
                "Odd uses the 1st and 3rd hole of each hole group (counted "
                "from its 32 mm system hole), Even the 2nd and 4th. Use "
                "opposite sets on the two faces of a shared carcass board so "
                "the screws don't meet."
            ),
        )
        self.front_setback = inputs.FloatInput(
            id="front_setback",
            name="Front Setback",
            default_value=0,
            tool_tip=(
                "Moves the slides back from the front edge, e.g. by the "
                "front thickness for inset drawer fronts."
            ),
            units=units,
        )
        # A value input created from the number 0 cannot report its
        # expression until the dialog is on screen.
        self.front_setback.default_expression = "0 mm"
        self.front_setback.minimum_value = 0
        self.flip_up = inputs.CheckboxInput(
            id="flip_up",
            name="Flip Up Direction",
            default_value=False,
            tool_tip=(
                "The screw rows go up from the Slide Heights along the world "
                "axis the front edges run along. Flip it for carcasses that "
                "are not modelled upright."
            ),
        )
        self.predrill_diameter = inputs.FloatInput(
            id="predrill_diameter",
            name="Pre-drill Diameter",
            default_value=0.2,
            tool_tip="Diameter of the pre-drill holes.",
            units=units,
        )
        self.predrill_diameter.minimum_value = 0.0001
        self.predrill_depth = inputs.FloatInput(
            id="predrill_depth",
            name="Pre-drill Depth",
            default_value=0.4,
            tool_tip="Depth of the flat-bottomed pre-drill holes.",
            units=units,
        )
        self.predrill_depth.minimum_value = 0.0001
        super().__init__()

    @staticmethod
    def nominal_length_id(model: drawer_slides.SlideModel) -> str:
        return f"nominal_length_{model.value}"

    def nominal_length(self, model: drawer_slides.SlideModel) -> inputs.DropDownInput:
        return getattr(self, self.nominal_length_id(model))


@dataclass(frozen=True)
class _Board:
    """A carcass side, seen from the face the slides mount to."""

    edge: adsk.fusion.BRepEdge
    face: adsk.fusion.BRepFace
    #: Start vertex of the front edge; heights are measured from here.
    origin: adsk.core.Point3D
    #: Along the front edge, upwards.
    up: adsk.core.Vector3D
    #: In the face, from the front edge towards the back.
    depth: adsk.core.Vector3D
    #: Normal of the face's plane (either sense).
    normal: adsk.core.Vector3D

    def height_of(self, point: adsk.core.Point3D) -> float:
        return self.origin.vectorTo(point).dotProduct(self.up)

    def project(self, point: adsk.core.Point3D) -> adsk.core.Point3D:
        """`point` moved onto the face's plane along its normal."""
        offset = self.origin.vectorTo(point).dotProduct(self.normal)
        return edge_sketch.translated(point, self.normal, -offset)

    def point_at(self, height: float, depth: float = 0.0) -> adsk.core.Point3D:
        point = edge_sketch.translated(self.origin, self.up, height)
        return edge_sketch.translated(point, self.depth, depth)

    def distance_to_edge(self, point: adsk.core.Point3D) -> float:
        return point.distanceTo(self.point_at(self.height_of(point)))


@dataclass(frozen=True)
class _Level:
    """One slide: the selected height reference and the points that can
    stand in for it in a sketch (a vertex or sketch point of a selected
    line)."""

    reference: adsk.core.Base
    candidates: list[tuple[adsk.core.Base, adsk.core.Point3D]]

    def nearest_candidate(self, board: _Board) -> tuple[adsk.core.Base, adsk.core.Point3D]:
        return min(
            self.candidates,
            key=lambda candidate: board.distance_to_edge(candidate[1]),
        )


@dataclass(frozen=True)
class _Plan:
    boards: list[_Board]
    #: Bottom to top.
    levels: list[_Level]
    #: Hole positions from the cabinet front edge, without the setback, cm.
    positions: list[float]
    setback: float


class DrawerSlides(addin.Addin):
    inputs: DrawerSlidesInputs
    _sketcher: edge_sketch.EdgeSketcher

    @property
    def resource_dir(self) -> str:
        # Absolute path so the command can also be (re)registered from outside
        # Fusion's add-in launcher (e.g. a scripted restart during development).
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources")

    @property
    def preview_enabled(self) -> bool:
        return True

    @property
    def group_edit_enabled(self) -> bool:
        return True

    @property
    def plugin_name(self) -> str:
        return NAME

    @property
    def plugin_desc(self) -> str:
        return "Pre-drill the cabinet holes for concealed drawer slides."

    @property
    def plugin_tooltip(self) -> str:
        return (
            "Creates fully constrained hole layouts and flat-bottomed "
            "pre-drill holes for Blum Movento and Grass Dynapro runners on "
            "the selected carcass sides."
        )

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

    def create_inputs(self) -> DrawerSlidesInputs:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise RuntimeError(f"{NAME} requires an active Fusion design.")
        return DrawerSlidesInputs(design.unitsManager)

    # Selection

    def pre_select(self, input, selection) -> bool:
        if not self.inputs or not input:
            return True
        if input.id == self.inputs.front_edges.id:
            edge = adsk.fusion.BRepEdge.cast(selection)
            if not (
                edge
                and edge.body
                and edge.body.isSolid
                and utils.brep.is_linear(edge)
                and utils.brep.largest_face_of_edge(edge)
            ):
                return False
            first = self._first_front_edge()
            return first is None or utils.brep.is_parallel(first, edge)
        if input.id == self.inputs.heights.id:
            if (
                adsk.fusion.BRepVertex.cast(selection)
                or adsk.fusion.SketchPoint.cast(selection)
                or adsk.fusion.ConstructionPoint.cast(selection)
            ):
                return True
            direction = self._line_direction(selection)
            if direction is None:
                return False
            first = self._first_front_edge()
            return first is None or utils.vector.is_perpendicular_direction(
                direction,
                utils.brep.normal_along_edge(first),
            )
        return True

    def _first_front_edge(self) -> adsk.fusion.BRepEdge | None:
        return next(
            (
                candidate
                for entity in self.inputs.front_edges.value
                if (candidate := adsk.fusion.BRepEdge.cast(entity))
            ),
            None,
        )

    def _line_direction(self, entity: adsk.core.Base) -> adsk.core.Vector3D | None:
        edge = adsk.fusion.BRepEdge.cast(entity)
        if edge:
            return utils.brep.normal_along_edge(edge) if utils.brep.is_linear(edge) else None
        line = adsk.fusion.SketchLine.cast(entity)
        if line:
            direction = line.startSketchPoint.worldGeometry.vectorTo(
                line.endSketchPoint.worldGeometry
            )
            return direction if direction.normalize() else None
        return None

    # Validation

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        self._apply_validation(args, self._validation_error)

    def _validation_error(self) -> str | None:
        try:
            self._plan()
        except ValueError as error:
            return str(error)
        return None

    def _plan(self) -> _Plan:
        """Resolves and checks the inputs; raises ValueError with a message
        for the dialog when they don't describe a buildable result."""
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise ValueError("An active Fusion design is required.")
        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:  # type: ignore
            raise ValueError(f"{NAME} requires Design History (a parametric design).")
        if not self.inputs or not self.inputs.front_edges.value:
            raise ValueError("Select the front edge of each carcass side.")
        if not self.inputs.heights.value:
            raise ValueError("Select a Slide Height for each slide.")

        boards = self._boards(design)
        levels = self._levels(design, boards[0])
        model = drawer_slides.slide_model(self.inputs.slide_type.value)
        nominal_length = self.inputs.nominal_length(model).value
        odd = self.inputs.hole_set.value == DrawerSlidesInputs.HoleSets.ODD.value
        candidates = drawer_slides.candidate_holes(model, nominal_length, odd)
        count = self.inputs.holes_per_slide.value
        if count > len(candidates):
            raise ValueError(
                f"{model.name} NL {nominal_length} offers only "
                f"{len(candidates)} {'odd' if odd else 'even'} holes."
            )
        positions = [
            position * MM
            for position in drawer_slides.choose_holes(candidates, count)
        ]
        setback = self.inputs.front_setback.value
        if setback < 0:
            raise ValueError("Front Setback can't be negative.")
        diameter = self.inputs.predrill_diameter.value
        depth = self.inputs.predrill_depth.value
        if diameter <= 0:
            raise ValueError("Pre-drill Diameter must be greater than zero.")
        if depth <= 0:
            raise ValueError("Pre-drill Depth must be greater than zero.")

        plan = _Plan(boards, levels, positions, setback)
        required_depth = (nominal_length + drawer_slides.DEPTH_ALLOWANCE) * MM + setback
        for index, board in enumerate(boards, 1):
            label = f"carcass side {index}" if len(boards) > 1 else "carcass side"
            try:
                thickness = utils.brep.get_board_thickness(board.face)
            except (ValueError, RuntimeError):
                raise ValueError(f"The {label} has no opposite face to drill into.")
            if depth >= thickness:
                raise ValueError(
                    f"Pre-drill Depth must be less than the {label}'s "
                    f"thickness ({_mm(thickness)})."
                )
            # Every side's runner starts at the first side's front edge.
            board_depth = max(
                boards[0].origin.vectorTo(vertex.geometry).dotProduct(boards[0].depth)
                for vertex in board.face.vertices
            )
            if required_depth > board_depth + SAME_POSITION:
                raise ValueError(
                    f"NL {nominal_length} needs {_mm(required_depth)} behind "
                    f"the front edge, but the {label} is only "
                    f"{_mm(board_depth)} deep."
                )
            if not self._holes_fit_face(plan, board, diameter):
                raise ValueError(
                    f"Some holes don't land on the {label}'s face. Check the "
                    "Slide Heights and the Up Direction."
                )
        return plan

    def _boards(self, design: adsk.fusion.Design) -> list[_Board]:
        edges: list[adsk.fusion.BRepEdge] = []
        for entity in self.inputs.front_edges.value:
            edge = adsk.fusion.BRepEdge.cast(entity)
            if not edge or not utils.brep.is_linear(edge):
                raise ValueError("Front Edges must be straight body edges.")
            edge = cast(adsk.fusion.BRepEdge, edge.nativeObject or edge)
            if not edge.body.isSolid:
                raise ValueError("Front Edges must belong to solid bodies.")
            if edge.body.parentComponent != design.activeComponent:
                raise ValueError(
                    "The carcass sides must be bodies of the active component."
                )
            edges.append(edge)
        if not all(utils.brep.is_parallel(edges[0], edge) for edge in edges):
            raise ValueError("The Front Edges must be parallel.")

        up = self._up_direction(utils.brep.normal_along_edge(edges[0]))
        boards: list[_Board] = []
        for edge in edges:
            face = utils.brep.largest_face_of_edge(edge)
            if not face:
                raise ValueError("Each Front Edge must border a planar board face.")
            if any(board.face == face for board in boards):
                raise ValueError(
                    "Two Front Edges border the same face. Select one front "
                    "edge per carcass side."
                )
            if any(board.face.body == face.body for board in boards):
                raise ValueError(
                    "Two Front Edges belong to the same board. For slides on "
                    "both faces of a shared board, run the command once per "
                    "side with opposite Hole Sets."
                )
            board = _Board(
                edge=edge,
                face=face,
                origin=edge.startVertex.geometry,
                up=up,
                depth=utils.brep.normal_into_face(edge, face),
                normal=adsk.core.Plane.cast(face.geometry).normal,
            )
            # The other sides take the first side's hole centers by
            # projection, which needs them facing the same way.
            if boards and not utils.brep.is_parallel(boards[0].face, face):
                raise ValueError("The carcass sides must be parallel.")
            if boards and not utils.vector.is_equal_direction(boards[0].depth, board.depth):
                raise ValueError(
                    "Select the front edges of all carcass sides; one of the "
                    "edges is at the back."
                )
            boards.append(board)
        return boards

    def _up_direction(self, edge_direction: adsk.core.Vector3D) -> adsk.core.Vector3D:
        """The world axis the front edges run along (Z, then Y, then X on a
        tie), pointing in its positive direction unless flipped."""
        axes = [
            adsk.core.Vector3D.create(0, 0, 1),
            adsk.core.Vector3D.create(0, 1, 0),
            adsk.core.Vector3D.create(1, 0, 0),
        ]
        axis = max(axes, key=lambda candidate: abs(candidate.dotProduct(edge_direction)))
        up = edge_direction.copy()
        if up.dotProduct(axis) < 0:
            up.scaleBy(-1)
        if self.inputs.flip_up.value:
            up.scaleBy(-1)
        return up

    def _levels(self, design: adsk.fusion.Design, board: _Board) -> list[_Level]:
        levels: list[_Level] = []
        for entity in self.inputs.heights.value:
            native = entity.nativeObject or entity  # type: ignore
            if self._component_of(native) != design.activeComponent:
                raise ValueError(
                    "Slide Heights must be geometry of the active component."
                )
            if adsk.fusion.BRepEdge.cast(native) or adsk.fusion.SketchLine.cast(native):
                direction = self._line_direction(native)
                if direction is None:
                    raise ValueError("Slide Height edges must be straight.")
                if not utils.vector.is_perpendicular_direction(direction, board.up):
                    raise ValueError(
                        "Slide Height edges and lines must be horizontal "
                        "(perpendicular to the Front Edges)."
                    )
            levels.append(_Level(native, self._candidates(native)))
        levels.sort(key=lambda level: board.height_of(level.candidates[0][1]))
        heights = [board.height_of(level.candidates[0][1]) for level in levels]
        if any(upper - lower < SAME_POSITION for lower, upper in zip(heights, heights[1:])):
            raise ValueError("Two Slide Heights are at the same height.")
        return levels

    def _component_of(self, entity: adsk.core.Base) -> adsk.fusion.Component | None:
        if vertex := adsk.fusion.BRepVertex.cast(entity):
            return vertex.body.parentComponent
        if edge := adsk.fusion.BRepEdge.cast(entity):
            return edge.body.parentComponent
        if point := adsk.fusion.SketchPoint.cast(entity):
            return point.parentSketch.parentComponent
        if line := adsk.fusion.SketchLine.cast(entity):
            return line.parentSketch.parentComponent
        if construction_point := adsk.fusion.ConstructionPoint.cast(entity):
            return construction_point.component
        return None

    def _candidates(self, entity: adsk.core.Base) -> list[tuple[adsk.core.Base, adsk.core.Point3D]]:
        """Points that can stand in for a height reference in a sketch.
        Lines and edges are represented by their end points: projecting a
        point is robust where projected lines are not (their end points
        don't follow a recompute)."""
        if vertex := adsk.fusion.BRepVertex.cast(entity):
            return [(vertex, vertex.geometry)]
        if point := adsk.fusion.SketchPoint.cast(entity):
            return [(point, point.worldGeometry)]
        if construction_point := adsk.fusion.ConstructionPoint.cast(entity):
            return [(construction_point, construction_point.geometry)]
        if edge := adsk.fusion.BRepEdge.cast(entity):
            return [
                (vertex, vertex.geometry)
                for vertex in (edge.startVertex, edge.endVertex)
            ]
        if line := adsk.fusion.SketchLine.cast(entity):
            return [
                (point, point.worldGeometry)
                for point in (line.startSketchPoint, line.endSketchPoint)
            ]
        raise ValueError("Slide Heights must be edges, sketch lines or points.")

    def _hole_centers(self, plan: _Plan, board: _Board, level: _Level) -> list[adsk.core.Point3D]:
        """The level's hole centers on `board`: laid out on the first side,
        and projected from there onto the other sides."""
        first = plan.boards[0]
        _, point = level.nearest_candidate(first)
        row = first.height_of(point) + drawer_slides.HOLE_ROW_HEIGHT * MM
        return [
            board.project(first.point_at(row, plan.setback + position))
            for position in plan.positions
        ]

    def _holes_fit_face(self, plan: _Plan, board: _Board, diameter: float) -> bool:
        tolerance = self.app.pointTolerance * 10
        radius = diameter / 2
        for level in plan.levels:
            for center in self._hole_centers(plan, board, level):
                probes = [center]
                for axis in (board.up, board.depth):
                    for sign in (-1, 1):
                        probes.append(edge_sketch.translated(center, axis, radius * sign))
                if not all(board.face.isPointOnFace(probe, tolerance) for probe in probes):
                    return False
        return True

    # Build

    def execute(self):
        plan = self._plan()
        self._sketcher = edge_sketch.EdgeSketcher(
            self._set_parameter_expression,
            self._name_parameter,
        )
        design = cast(adsk.fusion.Design, self.app.activeProduct)
        # All layouts first: they only project, while each hole feature
        # changes a body that a later layout might reference.
        count = len(plan.boards)
        first_sketch, first_points = self._create_layout(plan, plan.boards[0], count)
        layouts = [(plan.boards[0], first_sketch, first_points)]
        for index, board in enumerate(plan.boards[1:], 2):
            layouts.append((
                board,
                *self._create_projected_layout(plan, board, first_points, index, count),
            ))
        diameter_expression = self._expression(self.inputs.predrill_diameter)
        depth_expression = self._expression(self.inputs.predrill_depth)
        holes: list[adsk.fusion.HoleFeature] = []
        for index, (board, sketch, points) in enumerate(layouts, 1):
            face = edge_sketch.find_by_token(
                design,
                board.face.entityToken,
                adsk.fusion.BRepFace,
                "carcass side face",
            )
            hole = hole_features.create_simple_hole(
                face,
                sketch,
                points,
                diameter_expression,
                depth_expression,
                self._numbered(f"{NAME} - Pre-drill Holes", index, len(layouts)),
            )
            if not holes:
                # Later sides follow the first side's hole parameters.
                diameter_expression = hole.holeDiameter.name
                depth = hole_features.depth_parameter(hole)
                if depth:
                    depth_expression = depth.name
            holes.append(hole)
        if not self.group_features(layouts[0][1], holes[-1], NAME):
            raise RuntimeError(
                "Fusion created the drawer slide holes but could not group them."
            )

    def _numbered(self, name: str, index: int, count: int) -> str:
        return f"{name} {index}" if count > 1 else name

    def _expression(self, value_input: inputs.FloatInput) -> str:
        return value_input.expression or _mm(value_input.value)

    def _create_layout(
        self,
        plan: _Plan,
        board: _Board,
        count: int,
    ) -> tuple[adsk.fusion.Sketch, list[adsk.fusion.SketchPoint]]:
        """The hole centers of every slide on the first carcass side, fully
        constrained against the projected front edge and height references.

        Per slide: a construction line drops from the projected height
        reference onto the front edge (the runner's bottom), a segment along
        the front edge rises to the screw row, and the row runs into the
        face. Only the first slide is dimensioned (row height, setback, one
        distance per hole); the other rows reuse the row height through an
        equal constraint and line up their holes with the first slide's
        through construction lines parallel to the front edge."""
        context = self._sketcher.create_sketch(
            board.face.body.parentComponent,
            board.face,
            board.edge,
            self._numbered(f"{NAME} - Hole Layout", 1, count),
            "drawerSlides",
        )
        sketch = context.sketch
        front = context.edge_line
        references = self._project_references(sketch, plan, board)
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints

        def local(point: adsk.core.Point3D) -> adsk.core.Point3D:
            result = sketch.modelToSketchSpace(point)
            result.z = 0
            return result

        def construction_line(start, end) -> adsk.fusion.SketchLine:
            line = lines.addByTwoPoints(start, end)
            if not line:
                raise RuntimeError(f"Fusion failed to draw '{sketch.name}'.")
            line.isConstruction = True
            return line

        first_rise: adsk.fusion.SketchLine | None = None
        rows: list[list[adsk.fusion.SketchPoint]] = []
        expected: list[list[adsk.core.Point3D]] = []
        for level, reference in zip(plan.levels, references):
            _, reference_point = level.nearest_candidate(board)
            height = board.height_of(reference_point)
            base_target = local(board.point_at(height))
            if reference.geometry.distanceTo(base_target) <= SAME_POSITION:
                base = reference
            else:
                drop = construction_line(reference, base_target)
                constraints.addCoincident(drop.endSketchPoint, front)
                constraints.addPerpendicular(drop, front)
                base = drop.endSketchPoint

            row_height = drawer_slides.HOLE_ROW_HEIGHT * MM
            rise = construction_line(base, local(board.point_at(height + row_height)))
            constraints.addCoincident(rise.endSketchPoint, front)
            if first_rise is None:
                self._sketcher.add_distance_dimension(
                    sketch,
                    rise.startSketchPoint,
                    rise.endSketchPoint,
                    _mm(row_height),
                    "drawerSlidesRowHeight",
                )
                first_rise = rise
            else:
                constraints.addEqual(first_rise, rise)

            centers = self._hole_centers(plan, board, level)
            expected.append(centers)
            row = construction_line(rise.endSketchPoint, local(centers[-1]))
            constraints.addPerpendicular(row, front)
            points: list[adsk.fusion.SketchPoint] = []
            for center in centers[:-1]:
                point = sketch.sketchPoints.add(local(center))
                if not point:
                    raise RuntimeError(f"Fusion failed to draw '{sketch.name}'.")
                constraints.addCoincident(point, row)
                points.append(point)
            points.append(row.endSketchPoint)

            if not rows:
                # The first slide carries the dimensions.
                anchor = row.startSketchPoint
                if plan.setback > SAME_POSITION:
                    anchor = sketch.sketchPoints.add(
                        local(board.point_at(height + row_height, plan.setback))
                    )
                    constraints.addCoincident(anchor, row)
                    self._sketcher.add_distance_dimension(
                        sketch,
                        row.startSketchPoint,
                        anchor,
                        self._expression(self.inputs.front_setback),
                        "drawerSlidesSetback",
                    )
                for point, position in zip(points, plan.positions):
                    self._sketcher.add_distance_dimension(
                        sketch,
                        anchor,
                        point,
                        _mm(position),
                        "drawerSlidesHole",
                    )
            rows.append(points)

        if len(rows) > 1:
            for column in range(len(plan.positions)):
                column_line = construction_line(rows[0][column], rows[-1][column])
                constraints.addParallel(column_line, front)
                for row_points in rows[1:-1]:
                    constraints.addCoincident(row_points[column], column_line)

        self._sketcher.require_fully_constrained(sketch)
        for row_points, centers in zip(rows, expected):
            for point, center in zip(row_points, centers):
                if point.worldGeometry.distanceTo(center) > SAME_POSITION:
                    raise RuntimeError(
                        f"'{sketch.name}' solved to unexpected hole positions."
                    )
        return sketch, [point for row_points in rows for point in row_points]

    def _create_projected_layout(
        self,
        plan: _Plan,
        board: _Board,
        source_points: list[adsk.fusion.SketchPoint],
        index: int,
        count: int,
    ) -> tuple[adsk.fusion.Sketch, list[adsk.fusion.SketchPoint]]:
        """Another carcass side's hole centers: the first side's, projected.
        A drawer's runners sit at the same depth and height on both sides,
        so this layout carries no dimensions or constraints of its own and
        follows every change to the first one."""
        sketch = board.face.body.parentComponent.sketches.addWithoutEdges(board.face)
        if not sketch:
            raise RuntimeError(f"Fusion failed to create the hole layout of carcass side {index}.")
        sketch.name = self._numbered(f"{NAME} - Hole Layout", index, count)
        points = self._sketcher.project_points(
            sketch,
            source_points,
            "first carcass side's hole centers",
        )
        self._sketcher.require_fully_constrained(sketch)
        expected = [
            center
            for level in plan.levels
            for center in self._hole_centers(plan, board, level)
        ]
        for point, center in zip(points, expected):
            if point.worldGeometry.distanceTo(center) > SAME_POSITION:
                raise RuntimeError(
                    f"'{sketch.name}' projected to unexpected hole positions."
                )
        return sketch, points

    def _project_references(
        self,
        sketch: adsk.fusion.Sketch,
        plan: _Plan,
        board: _Board,
    ) -> list[adsk.fusion.SketchPoint]:
        """Projects each level's reference point (one batched project2
        call) and returns the projections in level order."""
        chosen = [level.nearest_candidate(board) for level in plan.levels]
        projected = [
            point
            for entity in self._sketcher.project_entities(
                sketch,
                [entity for entity, _ in chosen],
            )
            if (point := adsk.fusion.SketchPoint.cast(entity))
        ]
        if len(projected) != len(chosen):
            raise RuntimeError(
                f"Fusion failed to project the Slide Heights into '{sketch.name}'."
            )
        # project2 does not return the projections in input order.
        ordered: list[adsk.fusion.SketchPoint] = []
        for _, point in chosen:
            target = sketch.modelToSketchSpace(point)
            target.z = 0
            nearest = min(projected, key=lambda candidate: candidate.geometry.distanceTo(target))
            projected.remove(nearest)
            ordered.append(nearest)
        return ordered

    # Parameters

    def _set_parameter_expression(
        self,
        parameter: adsk.fusion.ModelParameter,
        expression: str,
    ) -> None:
        """Writes only expressions that carry a parametric link (e.g. a Front
        Setback given as a user parameter). Every dimension is created on
        geometry already at its value, so writing a literal would only
        change the displayed text - at the cost of a document update, ~0.5 s
        in a large assembly (see Addin._expression_references_parameter)."""
        if self._expression_references_parameter(expression):
            parameter.expression = expression

    def _name_parameter(
        self,
        parameter: adsk.fusion.ModelParameter,
        role: str,
    ) -> None:
        """Parameters keep Fusion's names (see AGENTS.md): every value here
        is edited through the dialog (group edit), and nothing depends on
        the names."""
        return
