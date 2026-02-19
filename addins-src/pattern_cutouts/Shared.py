import adsk.core
from lib import inputs, utils

type CoordinateSystem = tuple[adsk.core.Point3D, adsk.core.Vector3D, adsk.core.Vector3D, adsk.core.Vector3D]

class PatternInputs(inputs.Inputs):
    visibilities: list[tuple[set[int], list[inputs.Input]]]

    TRIANGLES = inputs.DropDownInput.Item('Triangles', 0)
    RHOMBUSES = inputs.DropDownInput.Item('Rhombuses', 1)
    FROLI = inputs.DropDownInput.Item('Froli', 4)
    ROUNDED_RECTANGLE = inputs.DropDownInput.Item('Rounded Rectangle', 3)
    CROSS = inputs.DropDownInput.Item('Cross', 2)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.faces = inputs.SelectionByEntityTokenInput(
            id='faces',
            name='Faces',
            filter=['PlanarFaces'],
            lower_bound=1,
            upper_bound=0,
            tool_tip='Select faces to create triangle pockets on.',
        )
        self.profiles = inputs.SelectionByEntityTokenInput(
            id='profiles',
            name='Profiles',
            filter=['Profiles'],
            lower_bound=0,
            upper_bound=0,
            tool_tip='Restrict the extent of the pattern to the selected profiles.',
        )
        self.scope = inputs.SelectionByEntityTokenInput(
            id='scope',
            name='Scope',
            filter=['Edges'],
            lower_bound=0,
            upper_bound=0,
            tool_tip='Restrict the extent of the pattern to area enclosing the selected edges.',
        )
        self.axis = inputs.SelectionByEntityTokenInput(
            id='axis',
            name='Axis',
            filter=['LinearEdges'],
            lower_bound=0,
            upper_bound=1,
            tool_tip='Select the axis for the pattern (optional).',
        )
        self.type = inputs.DropDownInput(
            id='type',
            name='Type',
            options=utils.misc.class_property_values(PatternInputs, inputs.DropDownInput.Item),
            default_value=PatternInputs.TRIANGLES.value,
            tool_tip='The type of pattern to use.',
        )
        self.preferred_width = inputs.FloatInput(
            id='preferred_width',
            name='Preferred Width',
            default_value=10,
            tool_tip='Indicates the preferred width of the shape.',
            units=units,
        )
        self.preferred_height = inputs.FloatInput(
            id='preferred_height',
            name='Preferred Height',
            default_value=15,
            tool_tip='Indicates the preferred height of the shape.',
            units=units,
        )
        self.spacing = inputs.FloatInput(
            id='spacing',
            name='Spacing',
            default_value=2,
            tool_tip='Spacing between the shapes.',
            units=units,
        )
        self.inset = inputs.FloatInput(
            id='inset',
            name='Inset',
            default_value=2,
            tool_tip='Inset of the pattern from the face\'s edges',
            units=units,
        )
        self.inner_loop_offset = inputs.FloatInput(
            id='inner_loop_offset',
            name='Inner Loop Offset',
            default_value=2,
            tool_tip='Material to keep around the inner loop of the face',
            units=units,
        )
        self.fillet = inputs.FloatInput(
            id='fillet',
            name='Fillet',
            default_value=0.8,
            tool_tip='Fillet radius',
            units=units,
        )
        self.compensate_fillet = inputs.CheckboxInput(
            id='compensate_fillet',
            name='Compensate Fillet',
            default_value=False,
            tool_tip='Makes all triangles in one row appear to be bottom and top aligned, irrespective of the fillet applied to the corners',
        )
        self.adaptive = inputs.CheckboxInput(
            id='adaptive',
            name='Adaptive',
            default_value=True,
            tool_tip='Prioritzes filling up the available space with the pattern over adhering to the width/height values, treating them more a starting point.',
        )
        self.tabs = inputs.CheckboxInput(
            id='tabs',
            name='Tabs',
            default_value=True,
            tool_tip='Creates tabs for inner loops to connect them to the outer perimeter of the shape.',
        )
        self.remainder = inputs.FloatInput(
            id='remainder',
            name='Remaining Material',
            default_value=0,
            tool_tip='Thickness of the remaining material to leave untouched.',
            units=units,
        )

        self.visibilities = [
            ({
                PatternInputs.TRIANGLES.value, 
                PatternInputs.RHOMBUSES.value, 
                PatternInputs.CROSS.value, 
                PatternInputs.ROUNDED_RECTANGLE.value, 
                PatternInputs.FROLI.value, 
            }, [
                self.faces,
                self.profiles,
                self.scope,
                self.type,
                self.inset,
                self.fillet,
                self.inner_loop_offset,
                self.remainder
            ]),
            ({
                PatternInputs.TRIANGLES.value, 
                PatternInputs.RHOMBUSES.value,
                PatternInputs.CROSS.value,
                PatternInputs.FROLI.value,
            }, [
                self.spacing
            ]),
            ({
                PatternInputs.TRIANGLES.value, 
                PatternInputs.RHOMBUSES.value,
                PatternInputs.CROSS.value,
            }, [
                self.axis,
            ]),
            ({
                PatternInputs.TRIANGLES.value, 
                PatternInputs.RHOMBUSES.value,
            }, [
                self.preferred_width,
                self.preferred_height,
                self.adaptive,
            ]),
            ({
                PatternInputs.CROSS.value,
                PatternInputs.ROUNDED_RECTANGLE.value,
            }, [
                self.tabs,
            ]),
            ({
                PatternInputs.TRIANGLES.value,
            }, [
                self.compensate_fillet,
            ]),
        ]
        super().__init__()

    def is_control_visible(self, input: inputs.Input) -> bool:
        for types, inputs in self.visibilities:
            if input in inputs:
                return self.type.value in types
        return False

    def update_visibilities(self):
        for input in self.inputs:
            if input.input and not self.is_control_visible(input):
                input.input.isVisible = False
        for types, inputs in self.visibilities:
            if self.type.value in types:
                for input in inputs:
                    if input.input:
                        input.input.isVisible = True
