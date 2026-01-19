# ConstructionPlaneOffsetThroughPointDefinition Object

Derived from: [ConstructionPlaneDefinition](ConstructionPlaneDefinition.md) Object  

## Description

Defines a construction plane that is offset from a planar face or construction plane and whose offset distance is defined by a vertex, sketch point, or construction point where the plane passes through the point.

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPlaneOffsetThroughPointDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [redefine](ConstructionPlaneOffsetThroughPointDefinition_redefine.md) | Redefines the input geometry of the construction plane. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConstructionPlaneOffsetThroughPointDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPlaneOffsetThroughPointDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionPlane](ConstructionPlaneOffsetThroughPointDefinition_parentConstructionPlane.md) | Returns the ConstructionPlane object |
| [planarEntity](ConstructionPlaneOffsetThroughPointDefinition_planarEntity.md) | Returns the planar face or construction plane this construction plane is parametrically dependent on. |
| [point](ConstructionPlaneOffsetThroughPointDefinition_point.md) | Returns the point that controls the offset. |

## Version

Introduced in version January 2025  

