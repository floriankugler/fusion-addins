# MachineAxis Object

Derived from: [Base](Base.md) Object  

## Description

Abstract base class representing a single machine axis.

## Methods

| Name | Description |
|----|----|
| [classType](MachineAxis_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [axisType](MachineAxis_axisType.md) | The type of axis. |
| [hasLimits](MachineAxis_hasLimits.md) | Does this axis have a limited range of motion. |
| [homePosition](MachineAxis_homePosition.md) | Specifies the value that this axis returns to when the machine is homed. Units are cm for linear axes or radians for rotary axes. Will return NaN if home position isn't set. |
| [isValid](MachineAxis_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](MachineAxis_name.md) | The name of this axis. |
| [objectType](MachineAxis_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [physicalRange](MachineAxis_physicalRange.md) | Range of possible values for this axis. Units are cm for linear axes or radians for rotary axes. |
| [toolChangePosition](MachineAxis_toolChangePosition.md) | Specifies the value that this axis returns to, prior to a tool change. Units are cm for linear axes or radians for rotary axes. Will return NaN if tool change position isn't set. |

## Accessed From

[MachinePart.axis](MachinePart_axis.md)

## Derived Classes

[LinearMachineAxis](LinearMachineAxis.md), [RotaryMachineAxis](RotaryMachineAxis.md)

## Version

Introduced in version April 2023  

