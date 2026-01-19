# Line3D Object

Derived from: [Curve3D](Curve3D.md) Object  

## Description

Transient 3D line. A transient line is not displayed or saved in a document. Transient 3D lines are used as a wrapper to work with raw 3D line information. They are created statically using the create method of the Line3D class.

## Methods

| Name | Description |
|----|----|
| [asInfiniteLine](Line3D_asInfiniteLine.md) | Creates an equivalent InfiniteLine3D. |
| [classType](Line3D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Line3D_copy.md) | Creates and returns a copy of this line object. |
| [create](Line3D_create.md) | Creates a transient line. |
| [getData](Line3D_getData.md) | Gets all of the data defining the line segment. |
| [intersectWithCurve](Line3D_intersectWithCurve.md) | Intersect this line with a curve to get the intersection point(s). |
| [intersectWithSurface](Line3D_intersectWithSurface.md) | Intersect this line with a surface to get the intersection point(s). |
| [isColinearTo](Line3D_isColinearTo.md) | Compare this line with another to check for collinearity |
| [set](Line3D_set.md) | Sets all of the data defining the line segment. |
| [transformBy](Line3D_transformBy.md) | Transforms this curve in 3D space. |

## Properties

| Name | Description |
| --- | --- |
| [asNurbsCurve](Line3D_asNurbsCurve.md) | Returns a NURBS curve that is geometrically identical to the line. |
| [curveType](Line3D_curveType.md) | Returns the type of geometry this curve represents. |
| [endPoint](Line3D_endPoint.md) | Gets and sets the end point of the line. |
| [evaluator](Line3D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isValid](Line3D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Line3D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [startPoint](Line3D_startPoint.md) | Gets and sets the start point of the line. |

## Accessed From

[Line3D.copy](Line3D_copy.md), [Line3D.create](Line3D_create.md), [SketchLine.geometry](SketchLine_geometry.md), [SketchLine.worldGeometry](SketchLine_worldGeometry.md)

## Version

Introduced in version August 2014  

