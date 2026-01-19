# ConstructionPlaneTangentAtPointDefinition Object

Derived from: [ConstructionPlaneDefinition](ConstructionPlaneDefinition.md) Object  

## Description

ConstructionPlaneTangentAtPointDefinition defines a ConstructionPlane tangent to a face and aligned to a point.

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPlaneTangentAtPointDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [redefine](ConstructionPlaneTangentAtPointDefinition_redefine.md) | Redefines the input geometry of the construction plane. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConstructionPlaneTangentAtPointDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPlaneTangentAtPointDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionPlane](ConstructionPlaneTangentAtPointDefinition_parentConstructionPlane.md) | Returns the ConstructionPlane object |
| [pointEntity](ConstructionPlaneTangentAtPointDefinition_pointEntity.md) | Gets the point (sketch point, vertex, construction point) used to align the plane. |
| [tangentFace](ConstructionPlaneTangentAtPointDefinition_tangentFace.md) | Gets the tangent face. |

## Version

Introduced in version August 2014  

