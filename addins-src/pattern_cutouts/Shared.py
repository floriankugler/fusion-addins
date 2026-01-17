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
        self.faces = inputs.SelectionByEntityTokenInput('faces', 'Faces', ['PlanarFaces'], 1, 0, 'Select faces to create triangle pockets on.')
        self.profiles = inputs.SelectionByEntityTokenInput('profiles', 'Profiles', ['Profiles'], 0, 0, 'Restrict the extent of the pattern to the selected profiles.')
        self.scope = inputs.SelectionByEntityTokenInput('scope', 'Scope', ['Edges'], 0, 0, 'Restrict the extent of the pattern to area enclosing the selected edges.')
        self.axis = inputs.SelectionByEntityTokenInput('axis', 'Axis', ['LinearEdges'], 0, 1, 'Select the axis for the pattern (optional).')
        self.type = inputs.DropDownInput('type', 'Type', utils.misc.class_property_values(PatternInputs, inputs.DropDownInput.Item), PatternInputs.TRIANGLES.value, 'The type of pattern to use.')
        self.preferred_width = inputs.FloatInput('preferred_width', 'Preferred Width', 10, 'Indicates the preferred width of the shape.', units)
        self.preferred_height = inputs.FloatInput('preferred_height', 'Preferred Height', 15, 'Indicates the preferred height of the shape.', units)
        self.spacing = inputs.FloatInput('spacing', 'Spacing', 2, 'Spacing between the shapes.', units)
        self.inset = inputs.FloatInput('inset', 'Inset', 2, 'Inset of the pattern from the face\'s edges', units)
        self.inner_loop_offset = inputs.FloatInput('inner_loop_offset', 'Inner Loop Offset', 2, 'Material to keep around the inner loop of the face', units)
        self.fillet = inputs.FloatInput('fillet', 'Fillet', 0.8, 'Fillet radius', units)
        self.compensate_fillet = inputs.CheckboxInput('compensate_fillet', 'Compensate Fillet', False, 'Makes all triangles in one row appear to be bottom and top aligned, irrespective of the fillet applied to the corners')
        self.adaptive = inputs.CheckboxInput('adaptive', 'Adaptive', True, 'Prioritzes filling up the available space with the pattern over adhering to the width/height values, treating them more a starting point.')
        self.tabs = inputs.CheckboxInput('tabs', 'Tabs', True, 'Creates tabs for inner loops to connect them to the outer perimeter of the shape.')
        self.remainder = inputs.FloatInput('remainder', 'Remaining Material', 0, 'Thickness of the remaining material to leave untouched.', units)

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

