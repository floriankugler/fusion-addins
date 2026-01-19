# Curve2D Object

Derived from: [Base](Base.md) Object  

## Description

The base class for all 2D transient geometry classes.

## Methods

| Name | Description |
|----|----|
| [classType](Curve2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [transformBy](Curve2D_transformBy.md) | Transforms this curve in 2D space. |

## Properties

| Name | Description |
| --- | --- |
| [curveType](Curve2D_curveType.md) | Returns the type of geometry this curve represents. |
| [evaluator](Curve2D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isValid](Curve2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Curve2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BRepCoEdge.geometry](BRepCoEdge_geometry.md)

## Derived Classes

[Arc2D](Arc2D.md), [Circle2D](Circle2D.md), [Ellipse2D](Ellipse2D.md), [EllipticalArc2D](EllipticalArc2D.md), [Line2D](Line2D.md), [NurbsCurve2D](NurbsCurve2D.md), [Polyline2D](Polyline2D.md)

## Version

Introduced in version August 2014  

