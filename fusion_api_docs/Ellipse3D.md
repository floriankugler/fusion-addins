# Ellipse3D Object

Derived from: [Curve3D](Curve3D.md) Object  

## Description

Transient 3D ellipse. A transient ellipse is n0t displayed or saved in a document. Transient 3D ellipses are used as a wrapper to work with raw 3D ellipse information. They are created statically using the create method of the Ellipse3D class.

## Methods

| Name | Description |
|----|----|
| [classType](Ellipse3D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Ellipse3D_copy.md) | Creates a copy of this Ellipse3D object. |
| [create](Ellipse3D_create.md) | Creates a transient 3D ellipse object. |
| [getData](Ellipse3D_getData.md) | Gets all of the data defining the ellipse. |
| [set](Ellipse3D_set.md) | Sets all of the data defining the ellipse. |
| [transformBy](Ellipse3D_transformBy.md) | Transforms this curve in 3D space. |

## Properties

| Name | Description |
| --- | --- |
| [asNurbsCurve](Ellipse3D_asNurbsCurve.md) | Returns a NURBS curve that is geometrically identical to the ellipse. |
| [center](Ellipse3D_center.md) | Gets and sets the center position of the ellipse. |
| [curveType](Ellipse3D_curveType.md) | Returns the type of geometry this curve represents. |
| [evaluator](Ellipse3D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isValid](Ellipse3D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [majorAxis](Ellipse3D_majorAxis.md) | Gets and sets the major axis of the ellipse. |
| [majorRadius](Ellipse3D_majorRadius.md) | Gets and sets the major radius of the ellipse. |
| [minorRadius](Ellipse3D_minorRadius.md) | Gets and sets the minor radius of the ellipse. |
| [normal](Ellipse3D_normal.md) | Gets the normal of the ellipse. |
| [objectType](Ellipse3D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Ellipse3D.copy](Ellipse3D_copy.md), [Ellipse3D.create](Ellipse3D_create.md), [SketchEllipse.geometry](SketchEllipse_geometry.md), [SketchEllipse.worldGeometry](SketchEllipse_worldGeometry.md)

## Version

Introduced in version August 2014  

