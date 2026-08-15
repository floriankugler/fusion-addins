"""Builds the multi-sheet envelope profile sketch.

The outline is a single closed profile: a row of BOTTOM-aligned rectangles
joined by thin gutters along their shared bottom edge. Bottom alignment
matters for nesting: Fusion's Arrange solver starts filling at the envelope's
minimum-Y/minimum-X region, so sheets of different heights must share their
bottom line — otherwise the tallest sheet reaches lowest and is filled first
regardless of sheet order. With a shared bottom line the leftmost sheet wins,
which puts offcuts first when they lead the row.

Shared between the envelope add-in (standalone command) and multi-arrange
(inline envelope creation).
"""

import adsk.core, adsk.fusion
from dataclasses import dataclass


# Spacing between adjacent rectangles and the height of the gutter that bridges
# it. Both are fixed by design but still become named sketch dimensions so the
# resulting sketch stays parametric.
SPACING_EXPRESSION = '100 mm'
GUTTER_HEIGHT_EXPRESSION = '5 mm'
SPACING = 10.0        # cm, Fusion internal units
GUTTER_HEIGHT = 0.5   # cm, Fusion internal units

DEFAULT_WIDTH_EXPRESSION = '200 mm'
DEFAULT_HEIGHT_EXPRESSION = '300 mm'

# A rectangle has to be taller than the gutter that bridges it. At exactly the
# gutter height the partial vertical edges collapse to zero length and the
# sketch can no longer be solved, so the limit is exclusive.
MINIMUM_HEIGHT = GUTTER_HEIGHT
MINIMUM_HEIGHT_EXPRESSION = GUTTER_HEIGHT_EXPRESSION


@dataclass
class RectangleSpec:
    """One row of the rectangles table."""
    width: float
    width_expression: str
    height: float
    height_expression: str
    count: int
    # Multi-arrange only: the sheet's grain runs along its width, so the
    # sheet enters the solve envelope rotated (grain is always envelope Y).
    # The envelope builder itself ignores this flag.
    grain_along_width: bool = False


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
class OffsetSpec:
    """An in-plane anchor offset along one model axis, as entered by the user."""
    value: float
    expression: str


def expand_rectangles(specs: list[RectangleSpec]) -> list[Rectangle]:
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


def unique_parameter_prefix(design: adsk.fusion.Design) -> str:
    parameter_names = {parameter.name for parameter in design.allParameters}
    base = 'envelope'
    index = 1
    while True:
        candidate = base if index == 1 else f'{base}{index}'
        if not any(name.startswith(f'{candidate}_') for name in parameter_names):
            return candidate
        index += 1


def validate_specs(specs: list[RectangleSpec]) -> str | None:
    """Returns an error message, or None when the table contents are valid."""
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
    return None


def build_envelope_sketch(
    component: adsk.fusion.Component,
    plane: adsk.fusion.ConstructionPlane,
    specs: list[RectangleSpec],
    sketch_name: str,
    in_plane_offsets: dict[str, OffsetSpec],
) -> adsk.fusion.Sketch:
    """Creates the fully constrained envelope sketch and returns it.

    `in_plane_offsets` maps model axis names ('X', 'Y', 'Z') to the offset of
    the first rectangle's bottom-left (gutter-side) corner along that axis;
    axes with no entry (or a zero value) are constrained to the sketch origin
    instead.
    """
    design = component.parentDesign
    if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:
        raise RuntimeError(
            'Envelope creation needs the parametric design mode to create named sketch dimensions.'
        )
    rectangles = expand_rectangles(specs)
    sketch = component.sketches.add(plane)
    sketch.name = sketch_name

    anchor, offsets = resolve_anchor(sketch, in_plane_offsets)
    builder = EnvelopeSketchBuilder(
        sketch,
        rectangles,
        unique_parameter_prefix(design),
        anchor,
        offsets,
    )
    builder.build()
    return sketch


def build_envelope_sketch_on(
    component: adsk.fusion.Component,
    plane_or_face,
    specs: list[RectangleSpec],
    sketch_name: str,
    x_offset: OffsetSpec | None = None,
    y_offset: OffsetSpec | None = None,
) -> adsk.fusion.Sketch:
    """Creates the envelope sketch on any construction plane or planar face.

    Unlike build_envelope_sketch, the offsets are applied along the sketch's
    own x/y axes, which works for arbitrarily oriented planes where model-axis
    offsets have no meaning. The offsets position the first rectangle's
    bottom-left (gutter-side) corner.
    """
    design = component.parentDesign
    if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:
        raise RuntimeError(
            'Envelope creation needs the parametric design mode to create named sketch dimensions.'
        )
    rectangles = expand_rectangles(specs)
    sketch = component.sketches.add(plane_or_face)
    sketch.name = sketch_name

    # Sketching on a body face auto-projects the face's edges, which would add
    # extra profiles and pollute the envelope. Demote any projected curves to
    # construction geometry so only the envelope outline forms a profile.
    for index in range(sketch.sketchCurves.count):
        curve = sketch.sketchCurves.item(index)
        if curve.isReference:
            try:
                curve.isConstruction = True
            except RuntimeError:
                pass

    anchor = adsk.core.Point3D.create(
        abs(x_offset.value) if x_offset else 0.0,
        abs(y_offset.value) if y_offset else 0.0,
        0.0,
    )
    offsets: dict[str, AnchorOffset] = {}
    if x_offset and abs(x_offset.value) > 1e-9:
        offsets['x'] = AnchorOffset(axis='X', expression=x_offset.expression)
    if y_offset and abs(y_offset.value) > 1e-9:
        offsets['y'] = AnchorOffset(axis='Y', expression=y_offset.expression)

    builder = EnvelopeSketchBuilder(
        sketch,
        rectangles,
        unique_parameter_prefix(design),
        anchor,
        offsets,
    )
    builder.build()
    return sketch


def resolve_anchor(
    sketch: adsk.fusion.Sketch,
    in_plane: dict[str, OffsetSpec],
) -> tuple[adsk.core.Point3D, dict[str, AnchorOffset]]:
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
        sketch_axis = sketch_axis_for_model_axis(sketch, axis)
        if sketch_axis is None:
            raise RuntimeError(f'The {axis} axis does not lie in the sketch plane.')
        offsets[sketch_axis] = AnchorOffset(axis=axis, expression=source.expression)
    return anchor, offsets


def sketch_axis_for_model_axis(sketch: adsk.fusion.Sketch, axis: str) -> str | None:
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


class EnvelopeSketchBuilder:
    """Builds the closed envelope profile and fully constrains it.

    The outline is a single closed loop of bottom-aligned rectangles. Walking
    it from the anchor (the first rectangle's bottom-left corner) it runs right
    along the shared bottom edge — alternating rectangle bottoms and gutter
    segments — up the right edge of the last rectangle, and then back along a
    zigzag: each rectangle's top, down its left edge to the gutter height,
    left across the gutter top, and up the previous rectangle's right edge.
    The first rectangle's left edge closes the loop.

    Because the loop merges the rectangles and gutters into one profile, the
    vertical edges of a rectangle start at the gutter height rather than the
    bottom edge, except for the outermost two. Heights are therefore
    dimensioned from the bottom edge up to the rectangle top, and repeated
    heights are tied together through the partial edges, which all share the
    same `height - gutter height` length.
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
        # The anchor is the first rectangle's bottom-left corner — the gutter
        # side of the sheet row — in sketch space. All geometry is laid out
        # relative to it.
        self.anchor = anchor
        self.anchor_offsets = anchor_offsets

        count = len(rectangles)
        self.tops: list[adsk.fusion.SketchLine] = [None] * count          # type: ignore
        self.bottoms: list[adsk.fusion.SketchLine] = [None] * count       # type: ignore
        self.left_edges: list[adsk.fusion.SketchLine] = [None] * count    # type: ignore
        self.right_edges: list[adsk.fusion.SketchLine] = [None] * count   # type: ignore
        # Gutter segments on the shared bottom line (forward pass) and at the
        # gutter height (return pass).
        self.gutter_bottoms: list[adsk.fusion.SketchLine] = [None] * max(0, count - 1)  # type: ignore
        self.gutter_tops: list[adsk.fusion.SketchLine] = [None] * max(0, count - 1)     # type: ignore

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

            # Forward pass: the shared bottom line, left to right.
            self.bottoms[0] = lines.addByTwoPoints(
                self._point(rectangles[0].left, 0.0),
                self._point(rectangles[0].right, 0.0),
            )
            cursor = self.bottoms[0]
            for index in range(1, last + 1):
                self.gutter_bottoms[index - 1] = lines.addByTwoPoints(
                    cursor.endSketchPoint,
                    self._point(rectangles[index].left, 0.0),
                )
                self.bottoms[index] = lines.addByTwoPoints(
                    self.gutter_bottoms[index - 1].endSketchPoint,
                    self._point(rectangles[index].right, 0.0),
                )
                cursor = self.bottoms[index]

            # Up the last rectangle's full right edge and across its top.
            last_rect = rectangles[last]
            self.right_edges[last] = lines.addByTwoPoints(
                cursor.endSketchPoint,
                self._point(last_rect.right, last_rect.height),
            )
            self.tops[last] = lines.addByTwoPoints(
                self.right_edges[last].endSketchPoint,
                self._point(last_rect.left, last_rect.height),
            )

            # Return pass: zigzag right to left across the gutters.
            for index in range(last, 0, -1):
                rectangle = rectangles[index]
                previous = rectangles[index - 1]
                self.left_edges[index] = lines.addByTwoPoints(
                    self.tops[index].endSketchPoint,
                    self._point(rectangle.left, GUTTER_HEIGHT),
                )
                self.gutter_tops[index - 1] = lines.addByTwoPoints(
                    self.left_edges[index].endSketchPoint,
                    self._point(previous.right, GUTTER_HEIGHT),
                )
                self.right_edges[index - 1] = lines.addByTwoPoints(
                    self.gutter_tops[index - 1].endSketchPoint,
                    self._point(previous.right, previous.height),
                )
                self.tops[index - 1] = lines.addByTwoPoints(
                    self.right_edges[index - 1].endSketchPoint,
                    self._point(previous.left, previous.height),
                )

            # Closing segment: the first rectangle's full left edge, reusing
            # the very first point so the loop closes on a shared sketch point.
            self.left_edges[0] = lines.addByTwoPoints(
                self.tops[0].endSketchPoint,
                self.bottoms[0].startSketchPoint,
            )
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

        # The bottom edges of the rectangles and the gutter segments share
        # endpoints and are all horizontal, which already makes them collinear.
        # Adding explicit collinear constraints on top of that would
        # over-constrain the sketch.

        # A rectangle's partial vertical edge is only tied to the bottom edge
        # through the gutter, so the bottom vertex below each partial edge needs
        # an explicit vertical alignment with the rectangle corner above it.
        for index in range(0, last):
            self._require(
                constraints.addVerticalPoints(
                    self.bottoms[index].endSketchPoint,
                    self.gutter_tops[index].endSketchPoint,
                ),
                'align a rectangle right edge with the bottom edge',
            )
        for index in range(1, last + 1):
            self._require(
                constraints.addVerticalPoints(
                    self.gutter_bottoms[index - 1].endSketchPoint,
                    self.left_edges[index].endSketchPoint,
                ),
                'align a rectangle left edge with the bottom edge',
            )

    def _anchor_profile(self):
        """Ties the first rectangle's bottom-left corner to the sketch origin.

        The bottom-left corner sits on the gutter side of the sheet row, which
        is the stable reference when sheet heights differ. With no offsets the
        corner is simply coincident with the origin. An axis that carries an
        offset gets a dimension instead, and an axis that does not still needs
        an alignment constraint to stay fully constrained.
        """
        constraints = self.sketch.geometricConstraints
        anchor = self.bottoms[0].startSketchPoint
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
                -self._text_offset(),
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
            text = self._point(rectangle.left - self._text_offset(), rectangle.height / 2)
            if first == 0:
                # The first rectangle's left edge spans the full height.
                dimension = self.sketch.sketchDimensions.addDistanceDimension(
                    self.left_edges[0].startSketchPoint,
                    self.left_edges[0].endSketchPoint,
                    adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,  # type: ignore
                    text,
                )
            else:
                # From the bottom-line vertex below the rectangle's left edge up
                # to its top-left corner.
                dimension = self.sketch.sketchDimensions.addDistanceDimension(
                    self.gutter_bottoms[first - 1].endSketchPoint,
                    self.tops[first].endSketchPoint,
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
        """The vertical edge of a rectangle that starts at the gutter height.

        Every rectangle has one as soon as there is more than one rectangle,
        and they all measure `height - gutter height`, which makes them the
        right curves to tie repeated heights together.
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
            GUTTER_HEIGHT + self._text_offset(),
        )
        spacing = self.sketch.sketchDimensions.addDistanceDimension(
            first_gutter.startSketchPoint,
            first_gutter.endSketchPoint,
            adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,  # type: ignore
            spacing_text,
        )
        self._name(spacing, 'spacing', SPACING_EXPRESSION)

        # The first gutter's top segment ends directly above the vertex that
        # ends the first rectangle's bottom edge.
        height_text = self._point(
            first_rect.right + self._text_offset(),
            GUTTER_HEIGHT / 2,
        )
        gutter_height = self.sketch.sketchDimensions.addDistanceDimension(
            self.bottoms[0].endSketchPoint,
            self.gutter_tops[0].endSketchPoint,
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
            # Holding the gutter tops at the same height repeats the gutter
            # height without a second dimension.
            self._require(
                constraints.addHorizontalPoints(
                    self.gutter_tops[0].endSketchPoint,
                    self.gutter_tops[index].endSketchPoint,
                ),
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
