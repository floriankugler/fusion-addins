import os

# All add-ins share the top-level module name 'lib', and whichever add-in loads
# first pins the package path for everyone. Make sure this add-in's own lib
# directory is searched as well before importing from it.
import lib
_ADDIN_LIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
if _ADDIN_LIB_DIR not in lib.__path__:
    lib.__path__.append(_ADDIN_LIB_DIR)

from lib import addin, inputs, ui_placement
from lib.envelope import builder
from lib.envelope.table_input import RectangleTableInput
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from typing import cast

_addin: addin.Addin | None = None


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = Envelope(runtime_info)
    # Dev support: allow external tooling to restart this add-in by firing the
    # custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'envelope.py')
    reloader.ensure(runtime_info.id + '_reload', entry)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


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

    def in_plane_offsets(self) -> dict[str, builder.OffsetSpec]:
        """The two axis offsets that lie in the selected sketch plane."""
        planes = EnvelopeInputs.Planes
        if self.plane.value == planes.XZ.value:
            selected = {'X': self.offset_x, 'Z': self.offset_z}
        elif self.plane.value == planes.YZ.value:
            selected = {'Y': self.offset_y, 'Z': self.offset_z}
        else:
            selected = {'X': self.offset_x, 'Y': self.offset_y}
        return {
            axis: builder.OffsetSpec(value=source.value, expression=source.expression)
            for axis, source in selected.items()
        }


class Envelope(addin.Addin):
    inputs: EnvelopeInputs

    @property
    def resource_dir(self) -> str:
        # Absolute path so the command can also be (re)registered from outside
        # Fusion's add-in launcher (e.g. a scripted restart during development).
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Resources')

    @property
    def plugin_name(self) -> str:
        return 'Envelope'

    @property
    def plugin_desc(self) -> str:
        return 'Creates a closed profile from a row of bottom-aligned rectangles'

    @property
    def plugin_tooltip(self) -> str:
        return (
            'Creates a sketch with a single closed profile: a row of '
            'bottom-aligned rectangles joined by thin gutters along the bottom '
            'edge. Bottom alignment makes Fusion\'s Arrange fill the sheets '
            'left to right.'
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
        message = builder.validate_specs(self.inputs.rectangles.value)
        if message:
            return message
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

        component = self.component
        builder.build_envelope_sketch(
            component,
            self._construction_plane(component),
            self.inputs.rectangles.value,
            self.inputs.sketch_name.value.strip(),
            self.inputs.in_plane_offsets(),
        )

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
