# SketchCircles Object

Derived from: [Base](Base.md) Object  

## Description

The collection of circles in a sketch. This provides access to the existing circles and supports the methods to create new circles.

## Methods

| Name | Description |
|----|----|
| [addByCenterRadius](SketchCircles_addByCenterRadius.md) | Creates a sketch circle that is always parallel to the x-y plane of the sketch and is centered at the specified point. |
| [addByThreePoints](SketchCircles_addByThreePoints.md) | Creates a sketch circle that passes through the three points. The three points must lie on the x-y plane of the sketch. |
| [addByThreeTangents](SketchCircles_addByThreeTangents.md) | Creates a sketch circle that is tangent to the three input lines. The three lines must lie on the x-y plane of the sketch. |
| [addByTwoPoints](SketchCircles_addByTwoPoints.md) | Creates a sketch circle where the circle passes through the two points and the distance between the two points is the diameter of the circle. |
| [addByTwoTangents](SketchCircles_addByTwoTangents.md) | Creates a sketch circle that is tangent to the two input lines. The two lines must lie on the x-y plane of the sketch. |
| [classType](SketchCircles_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SketchCircles_item.md) | Function that returns the specified sketch circle using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchCircles_count.md) | Returns the number of circles in the sketch. |
| [isValid](SketchCircles_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchCircles_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[SketchCurves.sketchCircles](SketchCurves_sketchCircles.md)

## Samples

| Name | Description |
|----|----|
| [Create circle by center and radius API Sample](CircleByCenterRadius_Sample.md) | Demonstrates creating a sketch circle by the center and radius. |
| [Create Circle By 3 Tangents API Sample](CreateCcircleBy3Tangents_Sample.md) | Creates three lines and then draws a circle that is tangent to the lines. It then creates tangent constraints to maintain that relationship. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |
| [SketchCircles.addByCenterRadius](SketchCircles_addByCenterRadius_Sample.md) | Demonstrates the SketchCircles.addByCenterRadius method. |
| [SketchCircles.addByThreePoints](SketchCircles_addByThreePoints_Sample.md) | Demonstrates the SketchCircles.addByThreePoints method. |
| [SketchCircles.addByThreeTangents](SketchCircles_addByThreeTangents_Sample.md) | Demonstrates the SketchCircles.addByThreeTangets method. |
| [SketchCircles.addByTwoPoints](SketchCircles_addByTwoPoints_Sample.md) | Demonstrates the SketchCircles.addByTwoPoints method. |
| [SketchCircles.addByTwoTangents](SketchCircles_addByTwoTangents_Sample.md) | Demonstrates the SketchCircles.addByTwoTangets method. |

## Version

Introduced in version August 2014  

