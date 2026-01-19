# NurbsCurve2D Object

Derived from: [Curve2D](Curve2D.md) Object  

## Description

Transient 2D NURBS curve. A transient NURBS curve is not displayed or saved in a document. Transient 2D NURBS curves are used as a wrapper to work with raw 2D NURBS curve information. They are created statically using one of the create methods of the NurbsCurve2D class.

## Methods

| Name | Description |
|----|----|
| [classType](NurbsCurve2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](NurbsCurve2D_copy.md) | Creates and returns an independent copy of this NurbsCurve2D object. |
| [createNonRational](NurbsCurve2D_createNonRational.md) | Creates a transient 2D NURBS non-rational b-spline object. |
| [createRational](NurbsCurve2D_createRational.md) | Creates a transient 2D NURBS rational b-spline object. |
| [extract](NurbsCurve2D_extract.md) | Defines a new NURBS curve that is the subset of this NURBS curve in the parameter range of \[startParam, endParam\] |
| [getData](NurbsCurve2D_getData.md) | Gets the data that defines a transient 2D NURBS rational b-spline object. |
| [merge](NurbsCurve2D_merge.md) | Define a new NURBS curve that is the result of combining this NURBS curve with another NURBS curve. The curves are merged with the end point of the current curve merging with the start point of the other curve. The curves are forced to join even if they are not physically touching so you will typically want to make sure the end and start points of the curves are where you expect them to be. |
| [reverse](NurbsCurve2D_reverse.md) | Reverses the orientation of the curve so the start and end points are swapped. The shape of the curve remains unchanged. This is especially useful to prepare the curves to use with the merge method. |
| [set](NurbsCurve2D_set.md) | Sets the data that defines a transient 2D NURBS rational b-spline object. |
| [transformBy](NurbsCurve2D_transformBy.md) | Transforms this curve in 2D space. |

## Properties

| Name | Description |
| --- | --- |
| [controlPointCount](NurbsCurve2D_controlPointCount.md) | Gets the number of control points that define the curve |
| [controlPoints](NurbsCurve2D_controlPoints.md) | Returns an array of Point2D objects that define the control points of the curve. |
| [curveType](NurbsCurve2D_curveType.md) | Returns the type of geometry this curve represents. |
| [degree](NurbsCurve2D_degree.md) | Returns the degree of the curve |
| [evaluator](NurbsCurve2D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isClosed](NurbsCurve2D_isClosed.md) | Returns if the curve is closed |
| [isPeriodic](NurbsCurve2D_isPeriodic.md) | Returns if the curve is periodic. |
| [isRational](NurbsCurve2D_isRational.md) | Returns if the curve is rational or non-rational type |
| [isValid](NurbsCurve2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [knotCount](NurbsCurve2D_knotCount.md) | Returns the knot count of the curve |
| [knots](NurbsCurve2D_knots.md) | Returns an array of numbers that define the Knots of the curve. |
| [objectType](NurbsCurve2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Arc2D.asNurbsCurve](Arc2D_asNurbsCurve.md), [Circle2D.asNurbsCurve](Circle2D_asNurbsCurve.md), [Ellipse2D.asNurbsCurve](Ellipse2D_asNurbsCurve.md), [EllipticalArc2D.asNurbsCurve](EllipticalArc2D_asNurbsCurve.md), [Line2D.asNurbsCurve](Line2D_asNurbsCurve.md), [NurbsCurve2D.copy](NurbsCurve2D_copy.md), [NurbsCurve2D.createNonRational](NurbsCurve2D_createNonRational.md), [NurbsCurve2D.createRational](NurbsCurve2D_createRational.md), [NurbsCurve2D.extract](NurbsCurve2D_extract.md), [NurbsCurve2D.merge](NurbsCurve2D_merge.md), [Polyline2D.asNurbsCurve](Polyline2D_asNurbsCurve.md)

## Version

Introduced in version August 2014  

