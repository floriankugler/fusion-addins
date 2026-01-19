# ConstructionPlaneDefinition Object

Derived from: [Base](Base.md) Object  

## Description

A Base class to return the information, possibly parametric, used to define the ConstructionPlane.

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPlaneDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConstructionPlaneDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPlaneDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionPlane](ConstructionPlaneDefinition_parentConstructionPlane.md) | Returns the ConstructionPlane object |

## Accessed From

[ConstructionPlane.definition](ConstructionPlane_definition.md)

## Derived Classes

[ConstructionPlaneAtAngleDefinition](ConstructionPlaneAtAngleDefinition.md), [ConstructionPlaneByPlaneDefinition](ConstructionPlaneByPlaneDefinition.md), [ConstructionPlaneDistanceOnPathDefinition](ConstructionPlaneDistanceOnPathDefinition.md), [ConstructionPlaneMidplaneDefinition](ConstructionPlaneMidplaneDefinition.md), [ConstructionPlaneOffsetDefinition](ConstructionPlaneOffsetDefinition.md), [ConstructionPlaneOffsetThroughPointDefinition](ConstructionPlaneOffsetThroughPointDefinition.md), [ConstructionPlaneTangentAtPointDefinition](ConstructionPlaneTangentAtPointDefinition.md), [ConstructionPlaneTangentDefinition](ConstructionPlaneTangentDefinition.md), [ConstructionPlaneThreePointsDefinition](ConstructionPlaneThreePointsDefinition.md), [ConstructionPlaneTwoEdgesDefinition](ConstructionPlaneTwoEdgesDefinition.md)

## Version

Introduced in version August 2014  

