# MachineAvoidDefaultSelection Object

Derived from: [MachineAvoidSelectionBase](MachineAvoidSelectionBase.md) Object  

## Description

Machine/avoid default selection class. Represents a group of selections that are parameter driven. Provides access to the stored selections.

## Methods

| Name | Description |
|----|----|
| [classType](MachineAvoidDefaultSelection_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [axialOffset](MachineAvoidDefaultSelection_axialOffset.md) | Axial offset - sets the corresponding axial offset value based on the machine mode |
| [combinedOffset](MachineAvoidDefaultSelection_combinedOffset.md) | Combined offset - clearance and stock to leave based on the machine mode This only applies to strategies that use a single offset value (Advanced Swarf, Multi-Axis Clearing, Multi-Axis Finishing, Deburr and Geodesic) |
| [error](MachineAvoidDefaultSelection_error.md) | Gets the last warning string encountered after the selection was applied to a parent. |
| [hasError](MachineAvoidDefaultSelection_hasError.md) | Gets if errors were encountered when applying the selection to a a parent. |
| [hasWarning](MachineAvoidDefaultSelection_hasWarning.md) | Gets if warnings were encountered when applying the selection to a parent. |
| [inputGeometry](MachineAvoidDefaultSelection_inputGeometry.md) | Get the value of the input geometry. |
| [isValid](MachineAvoidDefaultSelection_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [machineMode](MachineAvoidDefaultSelection_machineMode.md) | Desired machining mode. The default is Avoid. The current machining mode will determine which value the radial and axial offset functions refer to. When set to Machine, the radial and axial offset methods will read/set the stock to leave parameter. When set to Avoid, the radial and axial offset methods will read/set the clearance value, and the Fixture mode will map to the relative fixture clearance value. |
| [objectType](MachineAvoidDefaultSelection_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [radialOffset](MachineAvoidDefaultSelection_radialOffset.md) | Radial offset - sets the corresponding radial offset value based on the machine mode |
| [value](MachineAvoidDefaultSelection_value.md) | Returns the resulting value of the selection. In general, this returns the input selection, but child classes can override the return value if needed. Refer to the child classes comments for further details. The collection may contain duplicates. For OperationInputs, the return value may not be the same as for Operations, as additional geometry selected by child classes is not evaluated for OperationInputs. |
| [warning](MachineAvoidDefaultSelection_warning.md) | Gets the last warning string encountered after the selection was applied to a parent. |

## Version

Introduced in version September 2024  

