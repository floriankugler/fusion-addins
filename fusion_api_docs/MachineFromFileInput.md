# MachineFromFileInput Object

Derived from: [MachineInput](MachineInput.md) Object  

## Description

Object used as input to create a machine from a local file. It is used by the Machine.create method. The object holds the data needed to create a machine from a local machine file.

## Methods

| Name | Description |
|----|----|
| [classType](MachineFromFileInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](MachineFromFileInput_create.md) | Creates a MachineFromFileInput object to be used as input for Machine.create method. |

## Properties

| Name | Description |
| --- | --- |
| [filePath](MachineFromFileInput_filePath.md) | The path to a file to act as a base for creating a machine from. The filePath is expected to be an absolute path to the local machine file. |
| [ignoreSimulationModel](MachineFromFileInput_ignoreSimulationModel.md) | Whether or not to ignore the simulation model when creating/loading the machine. If set to true the simulation model will not be set on the new machine. |
| [isValid](MachineFromFileInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MachineFromFileInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[MachineFromFileInput.create](MachineFromFileInput_create.md)

## Version

Introduced in version April 2023  

