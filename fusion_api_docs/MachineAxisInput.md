# MachineAxisInput Object

Derived from: [Base](Base.md) Object  

## Description

Object that defines the properties required to create a machine axis object.

## Methods

| Name | Description |
|----|----|
| [classType](MachineAxisInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [axisType](MachineAxisInput_axisType.md) | The type of axis. This axis type determines which parameters of this object are valid to be accessed or modified. |
| [homePosition](MachineAxisInput_homePosition.md) | Specifies the value that this axis returns to when the machine is homed. Units are cm for linear axes or radians for rotary axes. |
| [isValid](MachineAxisInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](MachineAxisInput_name.md) | The user facing name of this axis. |
| [objectType](MachineAxisInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [physicalRange](MachineAxisInput_physicalRange.md) | Range of possible values for this axis. Units are cm for linear axes or radians for rotary axes. |
| [toolChangePosition](MachineAxisInput_toolChangePosition.md) | Specifies the value that this axis returns to, prior to a tool change. Units are cm for linear axes or radians for rotary axes. |

## Accessed From

[MachinePartInput.axisInput](MachinePartInput_axisInput.md), [MachinePartInput.createAxisInput](MachinePartInput_createAxisInput.md)

## Derived Classes

[LinearMachineAxisInput](LinearMachineAxisInput.md), [RotaryMachineAxisInput](RotaryMachineAxisInput.md)

## Version

Introduced in version April 2023  

