# RotaryMachineAxis Object

Derived from: [MachineAxis](MachineAxis.md) Object  

## Description

Object that represents an axis with rotary motion (e.g. A, B, and C).

## Methods

| Name | Description |
|----|----|
| [classType](RotaryMachineAxis_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [axisType](RotaryMachineAxis_axisType.md) | The type of axis. |
| [hasLimits](RotaryMachineAxis_hasLimits.md) | Does this axis have a limited range of motion. |
| [homePosition](RotaryMachineAxis_homePosition.md) | Specifies the value that this axis returns to when the machine is homed. Units are cm for linear axes or radians for rotary axes. Will return NaN if home position isn't set. |
| [isValid](RotaryMachineAxis_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](RotaryMachineAxis_name.md) | The name of this axis. |
| [objectType](RotaryMachineAxis_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [physicalRange](RotaryMachineAxis_physicalRange.md) | Range of possible values for this axis. Units are cm for linear axes or radians for rotary axes. |
| [rotationAxis](RotaryMachineAxis_rotationAxis.md) | The infinite line that defines the direction and location of the axis of rotation. |
| [toolChangePosition](RotaryMachineAxis_toolChangePosition.md) | Specifies the value that this axis returns to, prior to a tool change. Units are cm for linear axes or radians for rotary axes. Will return NaN if tool change position isn't set. |

## Version

Introduced in version April 2023  

