# MachineSpindle Object

Derived from: [Base](Base.md) Object  

## Description

Object representing a spindle on the machine

## Methods

| Name | Description |
|----|----|
| [classType](MachineSpindle_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [description](MachineSpindle_description.md) | The description of this spindle. |
| [isValid](MachineSpindle_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [maxSpeed](MachineSpindle_maxSpeed.md) | Specifies the maximum speed (rpm) for this spindle. |
| [minSpeed](MachineSpindle_minSpeed.md) | Specifies the minimum speed (rpm) for this spindle. |
| [objectType](MachineSpindle_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [peakTorque](MachineSpindle_peakTorque.md) | Specifies the peak torque (Nm) for this spindle. |
| [peakTorqueSpeed](MachineSpindle_peakTorqueSpeed.md) | Specifies the speed (rpm) at which this spindle reaches peak torque (Nm). |
| [power](MachineSpindle_power.md) | Specifies the power (kW) for this spindle. |

## Accessed From

[MachinePart.spindle](MachinePart_spindle.md)

## Version

Introduced in version April 2023  

