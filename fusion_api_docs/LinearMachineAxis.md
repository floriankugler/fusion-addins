# LinearMachineAxis Object

Derived from: [MachineAxis](MachineAxis.md) Object  

## Description

Object that represents an axis with linear motion (e.g. X, Y, and Z).

## Methods

| Name | Description |
|----|----|
| [classType](LinearMachineAxis_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [axisType](LinearMachineAxis_axisType.md) | The type of axis. |
| [direction](LinearMachineAxis_direction.md) | The unit vector that represents the direction along which the axis will move. |
| [hasLimits](LinearMachineAxis_hasLimits.md) | Does this axis have a limited range of motion. |
| [homePosition](LinearMachineAxis_homePosition.md) | Specifies the value that this axis returns to when the machine is homed. Units are cm for linear axes or radians for rotary axes. Will return NaN if home position isn't set. |
| [isValid](LinearMachineAxis_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](LinearMachineAxis_name.md) | The name of this axis. |
| [objectType](LinearMachineAxis_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [physicalRange](LinearMachineAxis_physicalRange.md) | Range of possible values for this axis. Units are cm for linear axes or radians for rotary axes. |
| [toolChangePosition](LinearMachineAxis_toolChangePosition.md) | Specifies the value that this axis returns to, prior to a tool change. Units are cm for linear axes or radians for rotary axes. Will return NaN if tool change position isn't set. |

## Version

Introduced in version April 2023  

