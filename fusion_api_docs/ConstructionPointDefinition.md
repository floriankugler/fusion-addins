# ConstructionPointDefinition Object

Derived from: [Base](Base.md) Object  

## Description

A Base class to return the information (possibly parametric) used to define a ConstructionPoint.

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPointDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConstructionPointDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPointDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionPoint](ConstructionPointDefinition_parentConstructionPoint.md) | Returns the ConstructionPoint object |

## Accessed From

[ConstructionPoint.definition](ConstructionPoint_definition.md)

## Derived Classes

[ConstructionPointCenterDefinition](ConstructionPointCenterDefinition.md), [ConstructionPointEdgePlaneDefinition](ConstructionPointEdgePlaneDefinition.md), [ConstructionPointPointDefinition](ConstructionPointPointDefinition.md), [ConstructionPointThreePlanesDefinition](ConstructionPointThreePlanesDefinition.md), [ConstructionPointTwoEdgesDefinition](ConstructionPointTwoEdgesDefinition.md)

## Version

Introduced in version August 2014  

