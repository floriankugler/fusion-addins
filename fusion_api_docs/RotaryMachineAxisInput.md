# RotaryMachineAxisInput Object

Derived from: [MachineAxisInput](MachineAxisInput.md) Object  

## Description

Object that defines the properties required to create a new rotary machine axis object.

## Methods

| Name | Description |
|----|----|
| [classType](RotaryMachineAxisInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [axisType](RotaryMachineAxisInput_axisType.md) | The type of axis. This axis type determines which parameters of this object are valid to be accessed or modified. |
| [homePosition](RotaryMachineAxisInput_homePosition.md) | Specifies the value that this axis returns to when the machine is homed. Units are cm for linear axes or radians for rotary axes. |
| [isValid](RotaryMachineAxisInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](RotaryMachineAxisInput_name.md) | The user facing name of this axis. |
| [objectType](RotaryMachineAxisInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [physicalRange](RotaryMachineAxisInput_physicalRange.md) | Range of possible values for this axis. Units are cm for linear axes or radians for rotary axes. |
| [rotationAxis](RotaryMachineAxisInput_rotationAxis.md) | The infinite line that defines the direction and location of the axis of rotation. This direction is in the machine's coordinate system (e.g. an A axis would typically use (1,0,0) for the direction), and follows the right-hand rule. |
| [toolChangePosition](RotaryMachineAxisInput_toolChangePosition.md) | Specifies the value that this axis returns to, prior to a tool change. Units are cm for linear axes or radians for rotary axes. |

## Version

Introduced in version April 2023  

