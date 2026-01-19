# SetupVisibilityManager Object

Derived from: [Base](Base.md) Object  

## Description

Class to manage the visibility of various elements of the setup.

## Methods

| Name | Description |
|----|----|
| [classType](SetupVisibilityManager_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](SetupVisibilityManager_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [machineBaseVisible](SetupVisibilityManager_machineBaseVisible.md) | Controls the visibility of the setup's machine base where it exists. This is always disabled for additive setups. |
| [machineVisible](SetupVisibilityManager_machineVisible.md) | Controls the visibility of the setup's machine. |
| [objectType](SetupVisibilityManager_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Setup.visibilityManager](Setup_visibilityManager.md)

## Version

Introduced in version January 2024  

