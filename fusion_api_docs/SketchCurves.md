# SketchCurves Object

Derived from: [Base](Base.md) Object  

## Description

A collection of sketch curves in a sketch. This also provides access to collections for the specific types of curves where you can get the curves based on type and create new curves.

## Methods

| Name | Description |
|----|----|
| [classType](SketchCurves_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SketchCurves_item.md) | Function that returns the specified sketch curve using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchCurves_count.md) | Returns the number of sketch curves in the sketch. |
| [isValid](SketchCurves_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchCurves_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sketchArcs](SketchCurves_sketchArcs.md) | Returns the sketch arcs collection associated with this sketch. This provides access to the existing sketch arcs and supports the creation of new sketch arcs. |
| [sketchCircles](SketchCurves_sketchCircles.md) | Returns the sketch circles collection associated with this sketch. This provides access to the existing sketch circles and supports the creation of new sketch circles. |
| [sketchConicCurves](SketchCurves_sketchConicCurves.md) | Returns the conic curves collection associated with this sketch. This provides access to the existing conic curves and supports the creation of new conic curves. |
| [sketchControlPointSplines](SketchCurves_sketchControlPointSplines.md) | Returns the control point splines collection associated with this sketch. This provides access to the existing control point splines and supports the creation of new control point splines. |
| [sketchEllipses](SketchCurves_sketchEllipses.md) | Returns the sketch ellipses collection associated with this sketch. This provides access to the existing sketch ellipses and supports the creation of new sketch ellipses. |
| [sketchEllipticalArcs](SketchCurves_sketchEllipticalArcs.md) | Returns the sketch elliptical arcs collection associated with this sketch. This provides access to the existing sketch elliptical arcs and supports the creation of new sketch elliptical arcs. |
| [sketchFittedSplines](SketchCurves_sketchFittedSplines.md) | Returns the sketch splines collection associated with this sketch. This provides access to the existing sketch splines and supports the creation of new sketch splines. |
| [sketchFixedSplines](SketchCurves_sketchFixedSplines.md) | Returns the fixed sketch splines collection associated with this sketch. This provides access to the existing fixed sketch splines and supports the creation of new fixed sketch splines. |
| [sketchLines](SketchCurves_sketchLines.md) | Returns the sketch lines collection associated with this sketch. This provides access to the existing sketch lines and supports the creation of new sketch lines. |

## Accessed From

[Sketch.sketchCurves](Sketch_sketchCurves.md)

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |

## Version

Introduced in version August 2014  

