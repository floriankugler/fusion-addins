from lib import addin, inputs, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from dataclasses import dataclass
from typing import cast

_addin: addin.Addin | None = None

# Spacing between adjacent rectangles and the height of the gutter that bridges
# it. Both are fixed by design but still become named sketch dimensions so the
# resulting sketch stays parametric.
SPACING_EXPRESSION = '100 mm'
GUTTER_HEIGHT_EXPRESSION = '5 mm'
SPACING = 10.0        # cm, Fusion internal units
GUTTER_HEIGHT = 0.5   # cm, Fusion internal units

DEFAULT_WIDTH_EXPRESSION = '200 mm'
DEFAULT_HEIGHT_EXPRESSION = '300 mm'

# A rectangle has to be deeper than the gutter that bridges it. At exactly the
# gutter height the partial vertical edges collapse to zero length and the
# sketch can no longer be solved, so the limit is exclusive.
MINIMUM_HEIGHT = GUTTER_HEIGHT
MINIMUM_HEIGHT_EXPRESSION = GUTTER_HEIGHT_EXPRESSION


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = Envelope(runtime_info)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


@dataclass
class RectangleSpec:
    """One row of the rectangles table."""
    width: float
    width_expression: str
    height: float
    height_expression: str
    count: int


@dataclass
class Rectangle:
    """One rectangle of the expanded row, i.e. after applying `count`."""
    width: float
    width_expression: str
    height: float
    height_expression: str
    left: float
    right: float


@dataclass
class AnchorOffset:
    """A non-zero offset of the anchor corner along one model axis."""
    axis: str          # 'X', 'Y' or 'Z', used to name the dimension parameter
    expression: str    # the expression the user typed, used verbatim


@dataclass
class TableRow:
    width: adsk.core.ValueCommandInput
    height: adsk.core.ValueCommandInput
    count: adsk.core.IntegerSpinnerCommandInput


class RectangleTableInput(inputs.Input):
    """A table of rectangle sizes with add / delete row buttons.

    Implemented here rather than in `lib/inputs.py` because a table has no
    counterpart in custom feature parameters, so it only works for the one-shot
    command style this add-in uses.
    """

    value: list[RectangleSpec]
    input: adsk.core.TableCommandInput

    def __init__(self, id: str, name: str, tool_tip: str, units: str):
        super().__init__(id, name, tool_tip, lambda: True)
        self.units = units
        self.value = []
        self._rows: list[TableRow] = []
        # Row inputs need ids that are unique for the lifetime of the dialog,
        # so the counter keeps rising instead of tracking the row index.
        self._next_row_key = 0
        self._add_button: adsk.core.BoolValueCommandInput | None = None
        self._delete_button: adsk.core.BoolValueCommandInput | None = None

    def create_input(self, command_inputs: adsk.core.CommandInputs, params: adsk.fusion.CustomFeatureParameters | None):
        if params is not None:
            raise RuntimeError("The rectangles table cannot be restored from a custom feature.")

        table = command_inputs.addTableCommandInput(self.id, self.name, 3, '2:2:1')
        table.minimumVisibleRows = 2
        table.maximumVisibleRows = 10
        table.hasGrid = False
        table.tablePresentationStyle = adsk.core.TablePresentationStyles.itemBorderTablePresentationStyle  # type: ignore
        self.input = table

        self._add_header_row()
        self._append_row(DEFAULT_WIDTH_EXPRESSION, DEFAULT_HEIGHT_EXPRESSION, 1)

        children = table.commandInputs
        self._add_button = children.addBoolValueInput(f'{self.id}_add', 'Add', False, '', False)
        self._add_button.tooltip = 'Add another rectangle size'
        self._delete_button = children.addBoolValueInput(f'{self.id}_delete', 'Delete', False, '', False)
        self._delete_button.tooltip = 'Delete the selected rectangle size'
        table.addToolbarCommandInput(self._add_button)
        table.addToolbarCommandInput(self._delete_button)

    def handle_input_changed(self, changed_input: adsk.core.CommandInput) -> bool:
        """Returns True when the change was a table button that was handled."""
        if not changed_input or self.input is None:
            return False

        if self._add_button and changed_input.id == self._add_button.id:
            self._add_button.value = False
            last = self._rows[-1] if self._rows else None
            self._append_row(
                self._expression_of(last.width, DEFAULT_WIDTH_EXPRESSION) if last else DEFAULT_WIDTH_EXPRESSION,
                self._expression_of(last.height, DEFAULT_HEIGHT_EXPRESSION) if last else DEFAULT_HEIGHT_EXPRESSION,
                int(last.count.value) if last else 1,
            )
            return True

        if self._delete_button and changed_input.id == self._delete_button.id:
            self._delete_button.value = False
            self._delete_selected_row()
            return True

        return False

    def update_from_input(self):
        specs: list[RectangleSpec] = []
        for row in self._rows:
            specs.append(RectangleSpec(
                width=row.width.value,
                width_expression=self._expression_of(row.width, DEFAULT_WIDTH_EXPRESSION),
                height=row.height.value,
                height_expression=self._expression_of(row.height, DEFAULT_HEIGHT_EXPRESSION),
                count=int(row.count.value),
            ))
        self.value = specs

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        raise RuntimeError("The rectangles table cannot be stored in a custom feature.")

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        raise RuntimeError("The rectangles table cannot be stored in a custom feature.")

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        raise RuntimeError("The rectangles table cannot be restored from a custom feature.")

    def _add_header_row(self):
        children = self.input.commandInputs
        for column, title in enumerate(('Width', 'Height', 'Count')):
            header = children.addStringValueInput(f'{self.id}_header_{column}', '', title)
            header.isReadOnly = True
            self.input.addCommandInput(header, 0, column, 0, 0)

    def _append_row(self, width_expression: str, height_expression: str, count: int):
        key = self._next_row_key
        self._next_row_key += 1
        children = self.input.commandInputs

        width = children.addValueInput(
            f'{self.id}_width_{key}',
            'Width',
            self.units,
            adsk.core.ValueInput.createByString(width_expression),
        )
        height = children.addValueInput(
            f'{self.id}_height_{key}',
            'Height',
            self.units,
            adsk.core.ValueInput.createByString(height_expression),
        )
        height.minimumValue = MINIMUM_HEIGHT
        height.isMinimumInclusive = False
        count_input = children.addIntegerSpinnerCommandInput(
            f'{self.id}_count_{key}',
            'Count',
            1,
            1000,
            1,
            max(1, count),
        )

        row_index = self.input.rowCount
        self.input.addCommandInput(width, row_index, 0, 0, 0)
        self.input.addCommandInput(height, row_index, 1, 0, 0)
        self.input.addCommandInput(count_input, row_index, 2, 0, 0)
        self._rows.append(TableRow(width, height, count_input))

    def _delete_selected_row(self):
        # The table always keeps one row so the command can never end up with
        # nothing to build.
        if len(self._rows) <= 1:
            return

        # Row 0 holds the header, so the row records are offset by one.
        selected = self.input.selectedRow
        row_index = selected if selected >= 1 else self.input.rowCount - 1
        record_index = row_index - 1
        if not 0 <= record_index < len(self._rows):
            return

        self.input.deleteRow(row_index)
        del self._rows[record_index]
        self.input.selectedRow = -1

    def _expression_of(self, value_input: adsk.core.ValueCommandInput, fallback: str) -> str:
        try:
            expression = value_input.expression
        except Exception:
            expression = None
        return expression if expression else fallback


class EnvelopeInputs(inputs.Inputs):
    class Planes:
        XY = inputs.DropDownInput.Item('X-Y', 0)
        XZ = inputs.DropDownInput.Item('X-Z', 1)
        YZ = inputs.DropDownInput.Item('Y-Z', 2)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        planes = EnvelopeInputs.Planes
        self.sketch_name = inputs.StringInput(
            id='sketch_name',
            name='Sketch name',
            default_value='Envelope',
            tool_tip='Name given to the created sketch',
        )
        self.plane = inputs.DropDownInput(
            id='plane',
            name='Sketch plane',
            options=[planes.XY, planes.XZ, planes.YZ],
            default_value=planes.XY.value,
            tool_tip='Construction plane of the active component to sketch on',
        )
        # One offset per model axis. The axis perpendicular to the sketch plane
        # is irrelevant, so it is hidden rather than silently ignored.
        self.offset_x = inputs.FloatInput(
            id='offset_x',
            name='X offset',
            default_value=0,
            tool_tip='Offset of the first rectangle corner from the origin along X',
            units=units,
            update_visibility=lambda: self.plane.value != planes.YZ.value,
        )
        self.offset_y = inputs.FloatInput(
            id='offset_y',
            name='Y offset',
            default_value=0,
            tool_tip='Offset of the first rectangle corner from the origin along Y',
            units=units,
            update_visibility=lambda: self.plane.value != planes.XZ.value,
        )
        self.offset_z = inputs.FloatInput(
            id='offset_z',
            name='Z offset',
            default_value=0,
            tool_tip='Offset of the first rectangle corner from the origin along Z',
            units=units,
            update_visibility=lambda: self.plane.value != planes.XY.value,
        )
        self.rectangles = RectangleTableInput(
            id='rectangles',
            name='Rectangles',
            tool_tip='Rectangle sizes, laid out left to right in table order',
            units=units,
        )
        super().__init__()

    def in_plane_offsets(self) -> dict[str, inputs.FloatInput]:
        """The two axis offsets that lie in the selected sketch plane."""
        planes = EnvelopeInputs.Planes
        if self.plane.value == planes.XZ.value:
            return {'X': self.offset_x, 'Z': self.offset_z}
        if self.plane.value == planes.YZ.value:
            return {'Y': self.offset_y, 'Z': self.offset_z}
        return {'X': self.offset_x, 'Y': self.offset_y}


class Envelope(addin.Addin):
    inputs: EnvelopeInputs

    @property
    def plugin_name(self) -> str:
        return 'Envelope'

    @property
    def plugin_desc(self) -> str:
        return 'Creates a closed profile from a row of top-aligned rectangles'

    @property
    def plugin_tooltip(self) -> str:
        return (
            'Creates a sketch with a single closed profile: a row of top-aligned '
            'rectangles joined by thin gutters.'
        )

    def get_ui_placement(self) -> ui_placement.UIPlacement:
        # The command creates its own sketch, so it belongs in the SOLID tab
        # next to Create Sketch rather than inside the sketch environment.
        # No separator section: remove_command_from_ui only deletes the command
        # control, so a separator would be left behind when the add-in unloads.
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id='SketchCreate',
        )
        return ui_placement.UIPlacement(
            panel_id='SolidCreatePanel',
            command=command,
        )

    def create_inputs(self) -> EnvelopeInputs:
        return EnvelopeInputs(self.app.activeProduct.unitsManager)

    def input_changed(self, input):
        if self.inputs:
            self.inputs.rectangles.handle_input_changed(input)

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        if self.inputs is None:
            return
        self.update_inputs_from_ui()
        message = self._input_error()
        self.showError(message)
        args.areInputsValid = message is None

    def _input_error(self) -> str | None:
        specs = self.inputs.rectangles.value
        if not specs:
            return 'Add at least one rectangle.'
        for index, spec in enumerate(specs, start=1):
            if spec.width <= 0:
                return f'Row {index}: width must be greater than zero.'
            if spec.height <= MINIMUM_HEIGHT:
                return (
                    f'Row {index}: height must be greater than '
                    f'{MINIMUM_HEIGHT_EXPRESSION}, the gutter height.'
                )
            if spec.count < 1:
                return f'Row {index}: count must be at least one.'
        if not self.inputs.sketch_name.value.strip():
            return 'Enter a sketch name.'
        return None

    def execute(self):
        error = self._input_error()
        if error:
            raise RuntimeError(error)

        design = cast(adsk.fusion.Design, self.app.activeProduct)
        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:  # type: ignore
            raise RuntimeError(
                'Envelope needs the parametric design mode to create named sketch dimensions.'
            )

        rectangles = self._expand_rectangles(self.inputs.rectangles.value)
        component = self.component
        sketch = component.sketches.add(self._construction_plane(component))
        sketch.name = self.inputs.sketch_name.value.strip()

        anchor, offsets = self._resolve_anchor(sketch)
        builder = EnvelopeSketchBuilder(
            sketch,
            rectangles,
            self._unique_parameter_prefix(design),
            anchor,
            offsets,
        )
        builder.build()

    def _construction_plane(self, component: adsk.fusion.Component) -> adsk.fusion.ConstructionPlane:
        # The profile is laid out in the sketch's own coordinate system, so it is
        # always top-aligned when the sketch is viewed face-on. Fusion's axes for
        # these planes are not all world-up (an X-Z sketch has its y axis along
        # negative Z, a Y-Z sketch its x axis along negative Z), so on those
        # planes the profile is mirrored or rotated in model space. That is
        # deliberate: it keeps the add-in consistent with Fusion's native axes.
        planes = EnvelopeInputs.Planes
        if self.inputs.plane.value == planes.XZ.value:
            return component.xZConstructionPlane
        if self.inputs.plane.value == planes.YZ.value:
            return component.yZConstructionPlane
        return component.xYConstructionPlane

    def _resolve_anchor(
        self,
        sketch: adsk.fusion.Sketch,
    ) -> tuple[adsk.core.Point3D, dict[str, 'AnchorOffset']]:
        """Maps the model-axis offsets onto the sketch's own axes.

        Returns the position to build at, in sketch space, plus for each sketch
        axis that carries a non-zero offset the model axis it came from. A sketch
        axis missing from the dict has no offset and gets a geometric constraint
        instead of a dimension.

        The build position uses the magnitude of each offset. Fusion always
        creates a distance dimension as a positive value measured towards
        wherever the point actually sits, so building on the positive side of
        each axis is what makes the dimension count in the positive model
        direction. The signed expression is then applied verbatim and the solver
        moves the profile to the correct side, which keeps the parameter reading
        exactly what the user typed.
        """
        in_plane = self.inputs.in_plane_offsets()

        build_position = adsk.core.Point3D.create(
            abs(in_plane['X'].value) if 'X' in in_plane else 0.0,
            abs(in_plane['Y'].value) if 'Y' in in_plane else 0.0,
            abs(in_plane['Z'].value) if 'Z' in in_plane else 0.0,
        )
        anchor = sketch.modelToSketchSpace(build_position)

        offsets: dict[str, AnchorOffset] = {}
        for axis, source in in_plane.items():
            if abs(source.value) <= 1e-9:
                continue
            sketch_axis = self._sketch_axis_for_model_axis(sketch, axis)
            if sketch_axis is None:
                raise RuntimeError(f'The {axis} axis does not lie in the sketch plane.')
            offsets[sketch_axis] = AnchorOffset(axis=axis, expression=source.expression)
        return anchor, offsets

    def _sketch_axis_for_model_axis(self, sketch: adsk.fusion.Sketch, axis: str) -> str | None:
        """Which sketch axis ('x'/'y') a model axis runs along, if any.

        Asking the sketch keeps this correct for each plane's own orientation
        instead of hard-coding it: an X-Z sketch, for example, has its y axis
        running along negative model Z.
        """
        unit = adsk.core.Point3D.create(
            1.0 if axis == 'X' else 0.0,
            1.0 if axis == 'Y' else 0.0,
            1.0 if axis == 'Z' else 0.0,
        )
        mapped = sketch.modelToSketchSpace(unit)
        if abs(mapped.x) > 0.5 and abs(mapped.y) < 1e-6:
            return 'x'
        if abs(mapped.y) > 0.5 and abs(mapped.x) < 1e-6:
            return 'y'
        return None

    def _expand_rectangles(self, specs: list[RectangleSpec]) -> list[Rectangle]:
        """Repeats every row `count` times and assigns the x placement."""
        rectangles: list[Rectangle] = []
        left = 0.0
        for spec in specs:
            for _ in range(spec.count):
                rectangles.append(Rectangle(
                    width=spec.width,
                    width_expression=spec.width_expression,
                    height=spec.height,
                    height_expression=spec.height_expression,
                    left=left,
                    right=left + spec.width,
                ))
                left += spec.width + SPACING
        return rectangles

    def _unique_parameter_prefix(self, design: adsk.fusion.Design) -> str:
        parameter_names = {parameter.name for parameter in design.allParameters}
        base = 'envelope'
        index = 1
        while True:
            candidate = base if index == 1 else f'{base}{index}'
            if not any(name.startswith(f'{candidate}_') for name in parameter_names):
                return candidate
            index += 1


class EnvelopeSketchBuilder:
    """Builds the closed envelope profile and fully constrains it.

    The outline is a single closed loop. Walking it counter-clockwise from the
    origin it runs up the left edge of the first rectangle, right along the
    shared top edge (alternating rectangle tops and gutter tops), down the right
    edge of the last rectangle, and then back to the origin along a zigzag: each
    rectangle bottom, up to the gutter bottom, left across the gutter, and down
    into the next rectangle.

    Because the loop merges the rectangles and gutters into one profile, the
    vertical edges of a rectangle only reach the gutter bottom rather than the
    top edge, except for the outermost two. Heights are therefore dimensioned
    from the top edge down to the rectangle bottom, and repeated heights are
    tied together through the partial edges, which all share the same
    `height - gutter height` length.
    """

    def __init__(
        self,
        sketch: adsk.fusion.Sketch,
        rectangles: list[Rectangle],
        parameter_prefix: str,
        anchor: adsk.core.Point3D,
        anchor_offsets: dict[str, AnchorOffset],
    ):
        self.sketch = sketch
        self.rectangles = rectangles
        self.parameter_prefix = parameter_prefix
        # The anchor is the first rectangle's bottom-left corner, in sketch
        # space. All geometry is laid out relative to it.
        self.anchor = anchor
        self.anchor_offsets = anchor_offsets
        self.top_y = rectangles[0].height

        count = len(rectangles)
        self.tops: list[adsk.fusion.SketchLine] = [None] * count          # type: ignore
        self.bottoms: list[adsk.fusion.SketchLine] = [None] * count       # type: ignore
        self.left_edges: list[adsk.fusion.SketchLine] = [None] * count    # type: ignore
        self.right_edges: list[adsk.fusion.SketchLine] = [None] * count   # type: ignore
        self.gutter_tops: list[adsk.fusion.SketchLine] = [None] * max(0, count - 1)     # type: ignore
        self.gutter_bottoms: list[adsk.fusion.SketchLine] = [None] * max(0, count - 1)  # type: ignore

    def build(self):
        self._create_outline()
        self._constrain_outline()
        self._dimension_widths()
        self._dimension_heights()
        self._dimension_gutters()

    # ---------------------------------------------------------------- geometry

    def _create_outline(self):
        # The geometry is created at its exact final coordinates, so every
        # constraint and dimension added afterwards is already satisfied and the
        # solver never has to move anything.
        self.sketch.isComputeDeferred = True
        try:
            lines = self.sketch.sketchCurves.sketchLines
            rectangles = self.rectangles
            last = len(rectangles) - 1

            first_rect = rectangles[0]
            self.left_edges[0] = lines.addByTwoPoints(
                self._point(first_rect.left, 0.0),
                self._point(first_rect.left, self.top_y),
            )
            cursor = self.left_edges[0]

            for index, rectangle in enumerate(rectangles):
                self.tops[index] = lines.addByTwoPoints(
                    cursor.endSketchPoint,
                    self._point(rectangle.right, self.top_y),
                )
                cursor = self.tops[index]
                if index < last:
                    self.gutter_tops[index] = lines.addByTwoPoints(
                        cursor.endSketchPoint,
                        self._point(rectangles[index + 1].left, self.top_y),
                    )
                    cursor = self.gutter_tops[index]

            last_rect = rectangles[last]
            self.right_edges[last] = lines.addByTwoPoints(
                cursor.endSketchPoint,
                self._point(last_rect.right, self.top_y - last_rect.height),
            )
            self.bottoms[last] = lines.addByTwoPoints(
                self.right_edges[last].endSketchPoint,
                # A single rectangle closes the loop on its bottom edge.
                self.left_edges[0].startSketchPoint if last == 0
                else self._point(last_rect.left, self.top_y - last_rect.height),
            )
            cursor = self.bottoms[last]

            for index in range(last, 0, -1):
                rectangle = rectangles[index]
                previous = rectangles[index - 1]
                self.left_edges[index] = lines.addByTwoPoints(
                    cursor.endSketchPoint,
                    self._point(rectangle.left, self.top_y - GUTTER_HEIGHT),
                )
                self.gutter_bottoms[index - 1] = lines.addByTwoPoints(
                    self.left_edges[index].endSketchPoint,
                    self._point(previous.right, self.top_y - GUTTER_HEIGHT),
                )
                self.right_edges[index - 1] = lines.addByTwoPoints(
                    self.gutter_bottoms[index - 1].endSketchPoint,
                    self._point(previous.right, self.top_y - previous.height),
                )
                if index - 1 == 0:
                    # Closing segment: reuse the very first point so the loop
                    # closes on a shared sketch point.
                    self.bottoms[0] = lines.addByTwoPoints(
                        self.right_edges[0].endSketchPoint,
                        self.left_edges[0].startSketchPoint,
                    )
                else:
                    self.bottoms[index - 1] = lines.addByTwoPoints(
                        self.right_edges[index - 1].endSketchPoint,
                        self._point(previous.left, self.top_y - previous.height),
                    )
                cursor = self.bottoms[index - 1]
        finally:
            self.sketch.isComputeDeferred = False

    def _point(self, x: float, y: float) -> adsk.core.Point3D:
        """Sketch point for a position measured from the anchor corner."""
        return adsk.core.Point3D.create(self.anchor.x + x, self.anchor.y + y, 0.0)

    # ------------------------------------------------------------- constraints

    def _constrain_outline(self):
        constraints = self.sketch.geometricConstraints
        last = len(self.rectangles) - 1

        self._anchor_profile()

        horizontals = list(self.tops) + list(self.bottoms) + list(self.gutter_tops) + list(self.gutter_bottoms)
        for line in horizontals:
            self._require(constraints.addHorizontal(line), 'make an edge horizontal')

        verticals = [self.left_edges[0], self.right_edges[last]]
        verticals += [self.left_edges[index] for index in range(1, last + 1)]
        verticals += [self.right_edges[index] for index in range(0, last)]
        for line in verticals:
            self._require(constraints.addVertical(line), 'make an edge vertical')

        # The top edges of the rectangles and the gutter tops share endpoints and
        # are all horizontal, which already makes them collinear. Adding explicit
        # collinear constraints on top of that would over-constrain the sketch.

        # A rectangle's partial vertical edge is only tied to the top edge through
        # the gutter, so the top vertex above each partial edge needs an explicit
        # vertical alignment with the rectangle corner below it.
        for index in range(0, last):
            self._require(
                constraints.addVerticalPoints(
                    self.tops[index].endSketchPoint,
                    self.bottoms[index].startSketchPoint,
                ),
                'align a rectangle right edge with the top edge',
            )
        for index in range(1, last + 1):
            self._require(
                constraints.addVerticalPoints(
                    self.gutter_tops[index - 1].endSketchPoint,
                    self.bottoms[index].endSketchPoint,
                ),
                'align a rectangle left edge with the top edge',
            )

    def _anchor_profile(self):
        """Ties the first rectangle's bottom-left corner to the sketch origin.

        With no offsets the corner is simply coincident with the origin. An axis
        that carries an offset gets a dimension instead, and an axis that does
        not still needs an alignment constraint to stay fully constrained.
        """
        constraints = self.sketch.geometricConstraints
        anchor = self.left_edges[0].startSketchPoint
        origin = self.sketch.originPoint
        offset_x = self.anchor_offsets.get('x')
        offset_y = self.anchor_offsets.get('y')

        if offset_x is None and offset_y is None:
            self._require(
                constraints.addCoincident(anchor, origin),
                'anchor the first rectangle to the sketch origin',
            )
            return

        if offset_x is None:
            # Vertically aligned points share an x coordinate.
            self._require(
                constraints.addVerticalPoints(origin, anchor),
                'align the anchor corner with the sketch origin',
            )
        else:
            self._dimension_anchor_offset(origin, anchor, offset_x, horizontal=True)

        if offset_y is None:
            self._require(
                constraints.addHorizontalPoints(origin, anchor),
                'align the anchor corner with the sketch origin',
            )
        else:
            self._dimension_anchor_offset(origin, anchor, offset_y, horizontal=False)

    def _dimension_anchor_offset(
        self,
        origin: adsk.fusion.SketchPoint,
        anchor: adsk.fusion.SketchPoint,
        offset: AnchorOffset,
        horizontal: bool,
    ):
        orientation = (
            adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation if horizontal
            else adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
        )  # type: ignore
        text = self._point(
            -self._text_offset() if horizontal else -2 * self._text_offset(),
            -2 * self._text_offset() if horizontal else -self._text_offset(),
        )
        dimension = self.sketch.sketchDimensions.addDistanceDimension(
            origin, anchor, orientation, text)
        # The profile was built on the positive side of this axis, so applying
        # the user's expression verbatim both keeps the parameter honest and lets
        # a negative value carry the geometry across the origin.
        self._name(dimension, f'offset{offset.axis}', offset.expression.strip())

    # ------------------------------------------------------------- dimensions

    def _dimension_widths(self):
        for indices in self._group_by(lambda rectangle: rectangle.width_expression):
            first = indices[0]
            rectangle = self.rectangles[first]
            bottom = self.bottoms[first]
            text = self._point(
                (rectangle.left + rectangle.right) / 2,
                self.top_y - rectangle.height - self._text_offset(),
            )
            dimension = self.sketch.sketchDimensions.addDistanceDimension(
                bottom.startSketchPoint,
                bottom.endSketchPoint,
                adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,  # type: ignore
                text,
            )
            self._name(dimension, f'rect{first + 1}_width', rectangle.width_expression)
            for other in indices[1:]:
                self._require(
                    self.sketch.geometricConstraints.addEqual(bottom, self.bottoms[other]),
                    'repeat a rectangle width',
                )

    def _dimension_heights(self):
        last = len(self.rectangles) - 1
        for indices in self._group_by(lambda rectangle: rectangle.height_expression):
            first = indices[0]
            rectangle = self.rectangles[first]
            text = self._point(rectangle.left - self._text_offset(), self.top_y - rectangle.height / 2)
            if first == 0:
                # The first rectangle's left edge spans the full height.
                dimension = self.sketch.sketchDimensions.addDistanceDimension(
                    self.left_edges[0].startSketchPoint,
                    self.left_edges[0].endSketchPoint,
                    adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,  # type: ignore
                    text,
                )
            else:
                dimension = self.sketch.sketchDimensions.addDistanceDimension(
                    self.bottoms[first].endSketchPoint,
                    self.gutter_tops[first - 1].endSketchPoint,
                    adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,  # type: ignore
                    text,
                )
            self._name(dimension, f'rect{first + 1}_height', rectangle.height_expression)

            for other in indices[1:]:
                self._require(
                    self.sketch.geometricConstraints.addEqual(
                        self._partial_vertical_edge(first, last),
                        self._partial_vertical_edge(other, last),
                    ),
                    'repeat a rectangle height',
                )

    def _partial_vertical_edge(self, index: int, last: int) -> adsk.fusion.SketchLine:
        """The vertical edge of a rectangle that stops at the gutter bottom.

        Every rectangle has one as soon as there is more than one rectangle, and
        they all measure `height - gutter height`, which makes them the right
        curves to tie repeated heights together.
        """
        if last == 0:
            raise RuntimeError('A single rectangle has no partial vertical edge.')
        return self.right_edges[0] if index == 0 else self.left_edges[index]

    def _dimension_gutters(self):
        if len(self.gutter_bottoms) == 0:
            return

        constraints = self.sketch.geometricConstraints
        first_gutter = self.gutter_bottoms[0]
        first_rect = self.rectangles[0]

        spacing_text = self._point(
            first_rect.right + SPACING / 2,
            self.top_y - GUTTER_HEIGHT - self._text_offset(),
        )
        spacing = self.sketch.sketchDimensions.addDistanceDimension(
            first_gutter.startSketchPoint,
            first_gutter.endSketchPoint,
            adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,  # type: ignore
            spacing_text,
        )
        self._name(spacing, 'spacing', SPACING_EXPRESSION)

        # The gutter bottom runs from the right edge of one rectangle to the left
        # edge of the next, so its endpoint sits directly below the top vertex
        # that ends the first rectangle's top edge.
        height_text = self._point(
            first_rect.right + self._text_offset(),
            self.top_y - GUTTER_HEIGHT / 2,
        )
        gutter_height = self.sketch.sketchDimensions.addDistanceDimension(
            first_gutter.endSketchPoint,
            self.tops[0].endSketchPoint,
            adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,  # type: ignore
            height_text,
        )
        self._name(gutter_height, 'gutterHeight', GUTTER_HEIGHT_EXPRESSION)

        for index in range(1, len(self.gutter_bottoms)):
            other = self.gutter_bottoms[index]
            self._require(
                constraints.addEqual(first_gutter, other),
                'repeat the rectangle spacing',
            )
            # Holding the gutter bottoms at the same height repeats the gutter
            # height without a second dimension.
            self._require(
                constraints.addHorizontalPoints(first_gutter.endSketchPoint, other.endSketchPoint),
                'repeat the gutter height',
            )

    # ------------------------------------------------------------------ helpers

    def _group_by(self, key) -> list[list[int]]:
        """Groups rectangle indices by a size expression, preserving order."""
        groups: dict[str, list[int]] = {}
        order: list[str] = []
        for index, rectangle in enumerate(self.rectangles):
            group_key = key(rectangle)
            if group_key not in groups:
                groups[group_key] = []
                order.append(group_key)
            groups[group_key].append(index)
        return [groups[group_key] for group_key in order]

    def _text_offset(self) -> float:
        """Distance used to place dimension text clear of the geometry."""
        return max(SPACING / 4, 1.0)

    def _name(self, dimension: adsk.fusion.SketchDimension, role: str, expression: str):
        if not dimension or not dimension.parameter:
            raise RuntimeError(f"Fusion failed to dimension the envelope '{role}'.")
        dimension.parameter.expression = expression
        name = f'{self.parameter_prefix}_{role}'
        dimension.parameter.name = name
        if dimension.parameter.name != name:
            raise RuntimeError(f"Fusion did not accept the parameter name '{name}'.")

    def _require(self, result, action: str):
        if not result:
            raise RuntimeError(f'Fusion failed to {action}.')
        return result
