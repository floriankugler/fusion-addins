# Polyline2D Object

Derived from: [Curve2D](Curve2D.md) Object  

## Description

Represents a single curve composed of a series of connected lines in 2D space.

## Methods

| Name | Description |
|----|----|
| [classType](Polyline2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](Polyline2D_create.md) | Creates a transient 2D polyline using an array of Point2D objects that defines the position of the polyline vertices. |
| [createByArray](Polyline2D_createByArray.md) | Creates a transient 2D polyline using an array of floating point values that specify the X, Y coordinates for each point. |
| [transformBy](Polyline2D_transformBy.md) | Transforms this curve in 2D space. |

## Properties

| Name | Description |
| --- | --- |
| [asNurbsCurve](Polyline2D_asNurbsCurve.md) | Returns a NURBS curve that is geometrically identical to the polyline. |
| [curveType](Polyline2D_curveType.md) | Returns the type of geometry this curve represents. |
| [evaluator](Polyline2D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isValid](Polyline2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Polyline2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [pointCount](Polyline2D_pointCount.md) | Returns the number of points defining the polyline. |
| [points](Polyline2D_points.md) | Gets and sets the points that define the coordinates of the polyline. |

## Accessed From

[Polyline2D.create](Polyline2D_create.md), [Polyline2D.createByArray](Polyline2D_createByArray.md)

## Version

Introduced in version September 2024  

