# MachineAxisConfigurations Object

Derived from: [Base](Base.md) Object  

## Description

Collection of axis configuration objects.

## Methods

| Name | Description |
|----|----|
| [addLinear](MachineAxisConfigurations_addLinear.md) | Add a new linear axis configuration for a kinematics part. |
| [addRotary](MachineAxisConfigurations_addRotary.md) | Add a new rotary axis configuration for a kinematics part. |
| [classType](MachineAxisConfigurations_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](MachineAxisConfigurations_item.md) | Get the configuration at index in this collection |
| [itemById](MachineAxisConfigurations_itemById.md) | Get the configuration with the given ID |

## Properties

| Name | Description |
| --- | --- |
| [count](MachineAxisConfigurations_count.md) | Get the number of configurations in the collection. |
| [isValid](MachineAxisConfigurations_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MachineAxisConfigurations_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ControllerConfigurationMachineElement.axisConfigurations](ControllerConfigurationMachineElement_axisConfigurations.md)

## Version

Introduced in version April 2023  

