# ConstructionPointPointDefinition Object

Derived from: [ConstructionPointDefinition](ConstructionPointDefinition.md) Object  

## Description

The definition for a parametric construction point created using the SetbyPoint method All non-parametric constructions points will return this type of definition regardless of the method used to initially create them.

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPointPointDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConstructionPointPointDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPointPointDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionPoint](ConstructionPointPointDefinition_parentConstructionPoint.md) | Returns the ConstructionPoint object |
| [pointEntity](ConstructionPointPointDefinition_pointEntity.md) | Gets and sets the position of the point using a construction point, sketch point or vertex. Non-parametric points will always return a Point3D object |

## Version

Introduced in version August 2014  

