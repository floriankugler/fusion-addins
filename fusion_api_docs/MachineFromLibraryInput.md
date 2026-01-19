# MachineFromLibraryInput Object

Derived from: [MachineInput](MachineInput.md) Object  

## Description

Object used as input to create a machine from library URL. Used by "Machine.create(MachineInput)" method. The object holds the data needed to create a machine from the specified library URL

## Methods

| Name | Description |
|----|----|
| [classType](MachineFromLibraryInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](MachineFromLibraryInput_create.md) | Creates a MachineFromLibraryInput object to be used as input for Machine.create method, in order to create a machine from a library location. |

## Properties

| Name | Description |
| --- | --- |
| [ignoreSimulationModel](MachineFromLibraryInput_ignoreSimulationModel.md) | Gets and sets whether or not to ignore the simulation model when creating or loading the machine. If set to true the simulation model will not be set on the new machine. |
| [isValid](MachineFromLibraryInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MachineFromLibraryInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [url](MachineFromLibraryInput_url.md) | The URL path to the library machine. |

## Accessed From

[MachineFromLibraryInput.create](MachineFromLibraryInput_create.md)

## Version

Introduced in version April 2023  

