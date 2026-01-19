# Line2D Object

Derived from: [Curve2D](Curve2D.md) Object  

## Description

Transient 2D line. A transient line is not displayed or saved in a document. Transient 2D lines are used as a wrapper to work with raw 2D line information. They are created statically using the create method of the Line2D class.

## Methods

| Name | Description |
|----|----|
| [classType](Line2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Line2D_copy.md) | Creates and returns a copy of this line object. |
| [create](Line2D_create.md) | Creates a transient line. |
| [getData](Line2D_getData.md) | Gets all of the data defining the line segment. |
| [set](Line2D_set.md) | Sets all of the data defining the line segment. |
| [transformBy](Line2D_transformBy.md) | Transforms this curve in 2D space. |

## Properties

| Name | Description |
| --- | --- |
| [asNurbsCurve](Line2D_asNurbsCurve.md) | Returns a NURBS curve that is geometrically identical to the line. |
| [curveType](Line2D_curveType.md) | Returns the type of geometry this curve represents. |
| [endPoint](Line2D_endPoint.md) | Gets and sets the end point of the line. |
| [evaluator](Line2D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isValid](Line2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Line2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [startPoint](Line2D_startPoint.md) | Gets and sets the start point of the line. |

## Accessed From

[Line2D.copy](Line2D_copy.md), [Line2D.create](Line2D_create.md)

## Version

Introduced in version August 2014  

