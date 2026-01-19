# MachineFromTemplateInput Object

Derived from: [MachineInput](MachineInput.md) Object  

## Description

Object used as input to create a machine from a given template. Used by "Machine.create(MachineInput)" method. The object holds the data needed to create a machine based on the specified template.

## Methods

| Name | Description |
|----|----|
| [classType](MachineFromTemplateInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](MachineFromTemplateInput_create.md) | Create a "MachineFromTemplateInput" object to be used as input for "Machine.create(MachineInput)" method. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](MachineFromTemplateInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [machineTemplate](MachineFromTemplateInput_machineTemplate.md) | Machine template identifier used to generate a certain type of machine. |
| [objectType](MachineFromTemplateInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[MachineFromTemplateInput.create](MachineFromTemplateInput_create.md)

## Version

Introduced in version April 2023  

