# ConstructionPointCenterDefinition Object

Derived from: [ConstructionPointDefinition](ConstructionPointDefinition.md) Object  

## Description

The definition for a parametric construction point created using the SetbyCenter method

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPointCenterDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [circularEntity](ConstructionPointCenterDefinition_circularEntity.md) | Gets and sets the spherical face (sphere or torus), circular edge or sketch arc/circle whose center defines the location for the construction point. |
| [isValid](ConstructionPointCenterDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPointCenterDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionPoint](ConstructionPointCenterDefinition_parentConstructionPoint.md) | Returns the ConstructionPoint object |

## Version

Introduced in version August 2014  

