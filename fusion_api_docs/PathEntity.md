# PathEntity Object

Derived from: [Base](Base.md) Object  

## Description

The PathEntity object represents a curve within a path

## Methods

| Name | Description |
|----|----|
| [classType](PathEntity_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](PathEntity_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](PathEntity_assemblyContext.md) | This property is not supported for a PathEntity object. |
| [curve](PathEntity_curve.md) | Property that returns the geometry of the entity. This is different from the original path curve if the true start point is not the same as the start point of the original path curve. |
| [curveType](PathEntity_curveType.md) | Property that returns the type of the curve referenced by the path entity. This property allows you to determine what type of object will be returned by the Curve property. |
| [entity](PathEntity_entity.md) | Property that gets the sketch curve or edge this entity was derived from. |
| [isOpposedToEntity](PathEntity_isOpposedToEntity.md) | Indicates if the orientation of this PathEntity is in the same direction or opposed to the natural direction of the SketchCurve or BRepEdge object it is derived from. |
| [isValid](PathEntity_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [nativeObject](PathEntity_nativeObject.md) | This property is not supported for a PathEntity object. |
| [objectType](PathEntity_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentPath](PathEntity_parentPath.md) | Property that returns the parent Path of the entity. |

## Accessed From

[Path.item](Path_item.md), [PathEntity.createForAssemblyContext](PathEntity_createForAssemblyContext.md), [PathEntity.nativeObject](PathEntity_nativeObject.md)

## Version

Introduced in version November 2014  

