# MachineSpindleInput Object

Derived from: [Base](Base.md) Object  

## Description

Object representing the set of inputs required to create a new MachineSpindle.

## Methods

| Name | Description |
|----|----|
| [classType](MachineSpindleInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [description](MachineSpindleInput_description.md) | The description of this spindle. |
| [isValid](MachineSpindleInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [maxSpeed](MachineSpindleInput_maxSpeed.md) | Specifies the maximum speed (rpm) for this spindle. |
| [minSpeed](MachineSpindleInput_minSpeed.md) | Specifies the minimum speed (rpm) for this spindle. |
| [objectType](MachineSpindleInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [peakTorque](MachineSpindleInput_peakTorque.md) | Specifies the peak torque for this spindle. |
| [peakTorqueSpeed](MachineSpindleInput_peakTorqueSpeed.md) | Specifies the peak torque speed for this spindle. |
| [power](MachineSpindleInput_power.md) | Specifies the power for this spindle. |

## Accessed From

[MachinePartInput.createSpindleInput](MachinePartInput_createSpindleInput.md), [MachinePartInput.spindleInput](MachinePartInput_spindleInput.md)

## Version

Introduced in version April 2023  

