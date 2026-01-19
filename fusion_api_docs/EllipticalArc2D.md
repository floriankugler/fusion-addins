# EllipticalArc2D Object

Derived from: [Curve2D](Curve2D.md) Object  

## Description

Transient 2D elliptical arc. A transient elliptical arc is not displayed or saved in a document. Transient 2D elliptical arcs are used as a wrapper to work with raw 2D elliptical arc information. They are created statically using the create method of the EllipticalArc2D class.

## Methods

| Name | Description |
|----|----|
| [classType](EllipticalArc2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](EllipticalArc2D_copy.md) | Creates and returns a copy of this EllipticalArc2D object. |
| [create](EllipticalArc2D_create.md) | Creates a transient 2D elliptical arc |
| [getData](EllipticalArc2D_getData.md) | Gets all of the data defining the elliptical arc. |
| [set](EllipticalArc2D_set.md) | Sets all of the data defining the elliptical arc. |
| [transformBy](EllipticalArc2D_transformBy.md) | Transforms this curve in 2D space. |

## Properties

| Name | Description |
| --- | --- |
| [asNurbsCurve](EllipticalArc2D_asNurbsCurve.md) | Returns a NURBS curve that is geometrically identical to the elliptical arc. |
| [center](EllipticalArc2D_center.md) | Gets and sets the center position of the elliptical arc. |
| [curveType](EllipticalArc2D_curveType.md) | Returns the type of geometry this curve represents. |
| [endAngle](EllipticalArc2D_endAngle.md) | Gets and sets the end angle of the elliptical arc in radians, where 0 is along the major axis. |
| [endPoint](EllipticalArc2D_endPoint.md) | Gets the position of the end point of the elliptical arc. |
| [evaluator](EllipticalArc2D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isCircular](EllipticalArc2D_isCircular.md) | Gets if the elliptical arc is the geometric equivalent of a circular arc |
| [isClockwise](EllipticalArc2D_isClockwise.md) | Gets if the sweep direction of the elliptical arc is clockwise or counterclockwise. |
| [isValid](EllipticalArc2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [majorAxis](EllipticalArc2D_majorAxis.md) | Gets and sets the major axis of the elliptical arc. |
| [majorRadius](EllipticalArc2D_majorRadius.md) | Gets and sets the major radius of the elliptical arc. |
| [minorRadius](EllipticalArc2D_minorRadius.md) | Gets and sets the minor radius of the elliptical arc. |
| [objectType](EllipticalArc2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [startAngle](EllipticalArc2D_startAngle.md) | Gets and sets the start angle of the elliptical arc in radians, where 0 is along the major axis. |
| [startPoint](EllipticalArc2D_startPoint.md) | Gets the position of the start point of the elliptical arc. |

## Accessed From

[EllipticalArc2D.copy](EllipticalArc2D_copy.md), [EllipticalArc2D.create](EllipticalArc2D_create.md)

## Version

Introduced in version August 2014  

