# BRepLoops Object

Derived from: [Base](Base.md) Object  

## Description

BRepLoop collection.

## Methods

| Name | Description |
|----|----|
| [classType](BRepLoops_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](BRepLoops_item.md) | Function that returns the specified loop using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](BRepLoops_count.md) | The number of loops in the collection. |
| [isValid](BRepLoops_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BRepLoops_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BRepFace.loops](BRepFace_loops.md)

## Samples

| Name | Description |
|----|----|
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version August 2014  

