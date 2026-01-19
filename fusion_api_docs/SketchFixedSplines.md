# SketchFixedSplines Object

Derived from: [Base](Base.md) Object  

## Description

The collection of fixed splines in a sketch. Fixed splines are splines that were created as the result of some operation (i.e. intersection) and is not directly editable.

## Methods

| Name | Description |
|----|----|
| [addByNurbsCurve](SketchFixedSplines_addByNurbsCurve.md) | Creates a new fixed spline using the input NurbsCurve3D to define the shape. The resulting curve is not editable by the user but can be updated via the API using the replaceGeometry method on the SketchFixedSpline object. |
| [classType](SketchFixedSplines_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SketchFixedSplines_item.md) | Function that returns the specified sketch fixed spline using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchFixedSplines_count.md) | Returns the number of fitted splines in the sketch. |
| [isValid](SketchFixedSplines_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchFixedSplines_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[SketchCurves.sketchFixedSplines](SketchCurves_sketchFixedSplines.md)

## Samples

| Name | Description |
|----|----|
| [SketchFixedSplines.addByNurbsCurve](SketchFixedSplines_addByNurbsCurve_Sample.md) | Demonstrates the SketchFixedSplines.addByNurbsCurve method. |

## Version

Introduced in version August 2014  

