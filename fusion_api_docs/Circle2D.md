# Circle2D Object

Derived from: [Curve2D](Curve2D.md) Object  

## Description

Transient 2D circle. A transient circle is not displayed or saved in a document. Transient circles are used as a wrapper to work with raw 2D arc information. They are created statically using one of the create methods of the Circle2D class.

## Methods

| Name | Description |
|----|----|
| [classType](Circle2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Circle2D_copy.md) | Creates and returns an independent copy of this Circle2D object. |
| [createByCenter](Circle2D_createByCenter.md) | Creates a transient 2D circle object by specifying a center and radius. |
| [createByThreePoints](Circle2D_createByThreePoints.md) | Creates a transient 2D circle through three points. |
| [getData](Circle2D_getData.md) | Gets all of the data defining the circle. |
| [set](Circle2D_set.md) | Sets all of the data defining the circle. |
| [transformBy](Circle2D_transformBy.md) | Transforms this curve in 2D space. |

## Properties

| Name | Description |
| --- | --- |
| [asNurbsCurve](Circle2D_asNurbsCurve.md) | Returns a NURBS curve that is geometrically identical to the circle. |
| [center](Circle2D_center.md) | Gets and sets the center position of the circle. |
| [curveType](Circle2D_curveType.md) | Returns the type of geometry this curve represents. |
| [evaluator](Circle2D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isValid](Circle2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Circle2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [radius](Circle2D_radius.md) | Gets and sets the radius of the circle. |

## Accessed From

[Circle2D.copy](Circle2D_copy.md), [Circle2D.createByCenter](Circle2D_createByCenter.md), [Circle2D.createByThreePoints](Circle2D_createByThreePoints.md)

## Version

Introduced in version August 2014  

