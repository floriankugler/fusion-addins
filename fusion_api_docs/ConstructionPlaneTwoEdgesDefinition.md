# ConstructionPlaneTwoEdgesDefinition Object

Derived from: [ConstructionPlaneDefinition](ConstructionPlaneDefinition.md) Object  

## Description

ConstructionPlaneTwoEdgesDefinition defines a ConstructionPlane by two co-planar linear entities like edges, sketch lines or construction axis.

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPlaneTwoEdgesDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [redefine](ConstructionPlaneTwoEdgesDefinition_redefine.md) | Redefines the input geometry of the construction plane. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConstructionPlaneTwoEdgesDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linearEntityOne](ConstructionPlaneTwoEdgesDefinition_linearEntityOne.md) | Gets the first linear edge, construction line, or sketch line that defines the construction plane. |
| [linearEntityTwo](ConstructionPlaneTwoEdgesDefinition_linearEntityTwo.md) | Gets the second linear edge, construction line, or sketch line that defines the construction plane. |
| [objectType](ConstructionPlaneTwoEdgesDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionPlane](ConstructionPlaneTwoEdgesDefinition_parentConstructionPlane.md) | Returns the ConstructionPlane object |

## Version

Introduced in version August 2014  

