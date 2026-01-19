# Arrange3DDefinition Object

Derived from: [ArrangeDefinition](ArrangeDefinition.md) Object  

## Description

This object defines all of the settings associated with a 3D arrangement.

## Methods

| Name | Description |
|----|----|
| [classType](Arrange3DDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isCreateCopies](Arrange3DDefinition_isCreateCopies.md) | Gets if the original components were moved to create the arrangement or copied were created. This value can only be set when creating a new arrangement. |
| [isValid](Arrange3DDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Arrange3DDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [solverType](Arrange3DDefinition_solverType.md) | Gets the type of arrange feature defined by this definition. |

## Version

Introduced in version January 2025  

