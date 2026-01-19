# Ellipse2D Object

Derived from: [Curve2D](Curve2D.md) Object  

## Description

Transient 2D ellipse. A transient ellipse is not displayed or saved in a document. Transient 2D ellipses are used as a wrapper to work with raw 2D ellipse information. They are created statically using the create method of the Ellipse2D class.

## Methods

| Name | Description |
|----|----|
| [classType](Ellipse2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Ellipse2D_copy.md) | Creates and returns a copy of this Ellipse2D object. |
| [create](Ellipse2D_create.md) | Creates a transient 2D ellipse by specifying a center position, major and minor axes, and major and minor radii. |
| [getData](Ellipse2D_getData.md) | Gets all of the data defining the ellipse. |
| [set](Ellipse2D_set.md) | Sets all of the data defining the ellipse. |
| [transformBy](Ellipse2D_transformBy.md) | Transforms this curve in 2D space. |

## Properties

| Name | Description |
| --- | --- |
| [asNurbsCurve](Ellipse2D_asNurbsCurve.md) | Returns a NURBS curve that is geometrically identical to the ellipse. |
| [center](Ellipse2D_center.md) | Gets and sets the center position of the ellipse. |
| [curveType](Ellipse2D_curveType.md) | Returns the type of geometry this curve represents. |
| [evaluator](Ellipse2D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isValid](Ellipse2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [majorAxis](Ellipse2D_majorAxis.md) | Gets and sets the major axis of the ellipse. |
| [majorRadius](Ellipse2D_majorRadius.md) | Gets and sets the major radius of the ellipse. |
| [minorRadius](Ellipse2D_minorRadius.md) | Gets and sets the minor radius of the ellipse. |
| [objectType](Ellipse2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Ellipse2D.copy](Ellipse2D_copy.md), [Ellipse2D.create](Ellipse2D_create.md)

## Version

Introduced in version August 2014  

