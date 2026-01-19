# MachineAxisRange Object

Derived from: [Base](Base.md) Object  

## Description

Class representing limits of motion for a machine axis.

## Methods

| Name | Description |
|----|----|
| [classType](MachineAxisRange_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](MachineAxisRange_create.md) | Creates a new range object with limited extents. Requires min to be less than or equal to max. Types of the fields depend on where this range is being used. Centimeters are used for distances and radians for angles. |
| [createInfinite](MachineAxisRange_createInfinite.md) | Creates a new unbounded range object. |

## Properties

| Name | Description |
| --- | --- |
| [isInfinite](MachineAxisRange_isInfinite.md) | Is the range infinite. |
| [isValid](MachineAxisRange_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [max](MachineAxisRange_max.md) | Maximum value of range Type depends on where this range is being used. Centimeters are used for distances and radians for angles. Returns infinity if this range is infinite. |
| [min](MachineAxisRange_min.md) | Minimum value of range. Type depends on where this range is being used. Centimeters are used for distances and radians for angles. Returns -infinity if this range is infinite. |
| [objectType](MachineAxisRange_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[LinearMachineAxis.physicalRange](LinearMachineAxis_physicalRange.md), [LinearMachineAxisInput.physicalRange](LinearMachineAxisInput_physicalRange.md), [MachineAxis.physicalRange](MachineAxis_physicalRange.md), [MachineAxisInput.physicalRange](MachineAxisInput_physicalRange.md), [MachineAxisRange.create](MachineAxisRange_create.md), [MachineAxisRange.createInfinite](MachineAxisRange_createInfinite.md), [RotaryMachineAxis.physicalRange](RotaryMachineAxis_physicalRange.md), [RotaryMachineAxisConfiguration.wrapAroundAtRange](RotaryMachineAxisConfiguration_wrapAroundAtRange.md), [RotaryMachineAxisInput.physicalRange](RotaryMachineAxisInput_physicalRange.md)

## Version

Introduced in version April 2023  

