# ConstructionPlaneDistanceOnPathDefinition Object

Derived from: [ConstructionPlaneDefinition](ConstructionPlaneDefinition.md) Object  

## Description

ConstructionDistanceOnPathDefinition defines a ConstructionPlane normal to an edge or sketch profile at a specified position along the path defined by the edge or sketch profile.

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPlaneDistanceOnPathDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [redefine](ConstructionPlaneDistanceOnPathDefinition_redefine.md) | Redefines the input defining the construction plane. |

## Properties

| Name | Description |
| --- | --- |
| [distance](ConstructionPlaneDistanceOnPathDefinition_distance.md) | Gets the distance along the path. |
| [isValid](ConstructionPlaneDistanceOnPathDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPlaneDistanceOnPathDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionPlane](ConstructionPlaneDistanceOnPathDefinition_parentConstructionPlane.md) | Returns the ConstructionPlane object |
| [pathEntity](ConstructionPlaneDistanceOnPathDefinition_pathEntity.md) | Gets the sketch curve, edge, or a profile object. |

## Version

Introduced in version August 2014  

