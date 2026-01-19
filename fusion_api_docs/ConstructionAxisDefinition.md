# ConstructionAxisDefinition Object

Derived from: [Base](Base.md) Object  

## Description

A Base class to return the information (possibly parametric) used to define a ConstructionAxis.

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionAxisDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConstructionAxisDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionAxisDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionAxis](ConstructionAxisDefinition_parentConstructionAxis.md) | Returns the ConstructionAxis object |

## Accessed From

[ConstructionAxis.definition](ConstructionAxis_definition.md)

## Derived Classes

[ConstructionAxisByLineDefinition](ConstructionAxisByLineDefinition.md), [ConstructionAxisCircularFaceDefinition](ConstructionAxisCircularFaceDefinition.md), [ConstructionAxisEdgeDefinition](ConstructionAxisEdgeDefinition.md), [ConstructionAxisNormalToFaceAtPointDefinition](ConstructionAxisNormalToFaceAtPointDefinition.md), [ConstructionAxisPerpendicularAtPointDefinition](ConstructionAxisPerpendicularAtPointDefinition.md), [ConstructionAxisTwoPlaneDefinition](ConstructionAxisTwoPlaneDefinition.md), [ConstructionAxisTwoPointDefinition](ConstructionAxisTwoPointDefinition.md)

## Version

Introduced in version August 2014  

