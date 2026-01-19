# SketchPoints Object

Derived from: [Base](Base.md) Object  

## Description

A collection of sketch points.

## Methods

| Name | Description |
|----|----|
| [add](SketchPoints_add.md) | Creates a point at the specified location. This is the equivalent of creating a sketch point using the Point command in the user interface and will create a visible point in the graphics window. |
| [classType](SketchPoints_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SketchPoints_item.md) | Function that returns the specified sketch using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchPoints_count.md) | Returns the number of sketch points in the sketch. |
| [isValid](SketchPoints_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchPoints_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Sketch.sketchPoints](Sketch_sketchPoints.md)

## Samples

| Name | Description |
|----|----|
| [GeometricConstraints.addCoincident](GeometricConstraints_addCoincident_Sample.md) | Demonstrates the GeometricConstraints.addCoincident method. |
| [SketchPoint.add](SketchPoint_add_Sample.md) | Demonstrates the SketchPoint.add method. |
| [Sketch Point API Sample](SketchPointSample_Sample.md) | Demonstrates creating a new sketch point. |

## Version

Introduced in version August 2014  

