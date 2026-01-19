# SketchEllipses Object

Derived from: [Base](Base.md) Object  

## Description

The collection of ellipses in a sketch. This provides access to the existing ellipses and supports the methods to create new ellipses.

## Methods

| Name | Description |
|----|----|
| [add](SketchEllipses_add.md) | Creates a sketch ellipse using the center point, a point defining the major axis and a third point anywhere along the ellipse. The created ellipse is parallel to the x-y plane of the sketch. |
| [classType](SketchEllipses_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SketchEllipses_item.md) | Function that returns the specified sketch ellipse using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchEllipses_count.md) | Returns the number of ellipses in the sketch. |
| [isValid](SketchEllipses_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchEllipses_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[SketchCurves.sketchEllipses](SketchCurves_sketchEllipses.md)

## Version

Introduced in version August 2014  

