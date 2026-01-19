# SketchControlPointSplines Object

Derived from: [Base](Base.md) Object  

## Description

The collection of control point splines in a sketch.

## Methods

| Name | Description |
|----|----|
| [add](SketchControlPointSplines_add.md) | Creates a new control point spline. |
| [classType](SketchControlPointSplines_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SketchControlPointSplines_item.md) | Function that returns the specified sketch control point spline using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchControlPointSplines_count.md) | Returns the number of control point splines in the sketch. |
| [isValid](SketchControlPointSplines_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchControlPointSplines_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[SketchCurves.sketchControlPointSplines](SketchCurves_sketchControlPointSplines.md)

## Version

Introduced in version July 2022  

