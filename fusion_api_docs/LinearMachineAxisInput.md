# LinearMachineAxisInput Object

Derived from: [MachineAxisInput](MachineAxisInput.md) Object  

## Description

Object that defines the properties required to create a new linear machine axis object.

## Methods

| Name | Description |
|----|----|
| [classType](LinearMachineAxisInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [axisType](LinearMachineAxisInput_axisType.md) | The type of axis. This axis type determines which parameters of this object are valid to be accessed or modified. |
| [direction](LinearMachineAxisInput_direction.md) | The unit vector that represents the direction along which the linear axis will move. This vector is in the machine's coordinate system (e.g. the X axis is always (1,0,0)). |
| [homePosition](LinearMachineAxisInput_homePosition.md) | Specifies the value that this axis returns to when the machine is homed. Units are cm for linear axes or radians for rotary axes. |
| [isValid](LinearMachineAxisInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](LinearMachineAxisInput_name.md) | The user facing name of this axis. |
| [objectType](LinearMachineAxisInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [physicalRange](LinearMachineAxisInput_physicalRange.md) | Range of possible values for this axis. Units are cm for linear axes or radians for rotary axes. |
| [toolChangePosition](LinearMachineAxisInput_toolChangePosition.md) | Specifies the value that this axis returns to, prior to a tool change. Units are cm for linear axes or radians for rotary axes. |

## Version

Introduced in version April 2023  

