# Circle3D Object

Derived from: [Curve3D](Curve3D.md) Object  

## Description

Transient 3D circle. A transient circle is not displayed or saved in a document. Transient 3D circles are used as a wrapper to work with raw 3D circle information. They are created statically using one of the create methods of the Circle3D class.

## Methods

| Name | Description |
|----|----|
| [classType](Circle3D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Circle3D_copy.md) | Creates and returns an independent copy of this Circle3D object. |
| [createByCenter](Circle3D_createByCenter.md) | Creates a transient 3D circle object by specifying a center and radius. |
| [createByThreePoints](Circle3D_createByThreePoints.md) | Creates a transient 3D circle through three points. |
| [getData](Circle3D_getData.md) | Gets all of the data defining the circle. |
| [set](Circle3D_set.md) | Sets all of the data defining the circle. |
| [transformBy](Circle3D_transformBy.md) | Transforms this curve in 3D space. |

## Properties

| Name | Description |
| --- | --- |
| [asNurbsCurve](Circle3D_asNurbsCurve.md) | Returns a NURBS curve that is geometrically identical to the circle. |
| [center](Circle3D_center.md) | Gets and sets the center position of the circle. |
| [curveType](Circle3D_curveType.md) | Returns the type of geometry this curve represents. |
| [evaluator](Circle3D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isValid](Circle3D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [normal](Circle3D_normal.md) | Gets and sets the normal of the circle. |
| [objectType](Circle3D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [radius](Circle3D_radius.md) | Gets and sets the radius of the circle. |

## Accessed From

[Circle3D.copy](Circle3D_copy.md), [Circle3D.createByCenter](Circle3D_createByCenter.md), [Circle3D.createByThreePoints](Circle3D_createByThreePoints.md), [SketchCircle.geometry](SketchCircle_geometry.md), [SketchCircle.worldGeometry](SketchCircle_worldGeometry.md)

## Samples

| Name | Description |
|----|----|
| [Get Circle and Arc Data from Edge API Sample](GetCircleAndArcDataFromEdge_Sample.md) | Display the arc and circle geometric information from a selected circular edge. |

## Version

Introduced in version August 2014  

