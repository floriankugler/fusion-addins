# ConstructionPointTwoEdgesDefinition Object

Derived from: [ConstructionPointDefinition](ConstructionPointDefinition.md) Object  

## Description

The definition for a parametric construction point created using the SetbyTwoEdges method

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPointTwoEdgesDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [redefine](ConstructionPointTwoEdgesDefinition_redefine.md) | Redefines the input geometry of the construction point. |

## Properties

| Name | Description |
| --- | --- |
| [edgeOne](ConstructionPointTwoEdgesDefinition_edgeOne.md) | Returns a B-Rep edge or sketch line |
| [edgeTwo](ConstructionPointTwoEdgesDefinition_edgeTwo.md) | Returns a B-Rep edge or sketch line |
| [isValid](ConstructionPointTwoEdgesDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPointTwoEdgesDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionPoint](ConstructionPointTwoEdgesDefinition_parentConstructionPoint.md) | Returns the ConstructionPoint object |

## Version

Introduced in version August 2014  

