# Arc2D Object

Derived from: [Curve2D](Curve2D.md) Object  

## Description

Transient 2D arc. A transient arc is not displayed or saved in a document. Transient arcs are used as a wrapper to work with raw 2D arc information. They are created statically using one of the create methods supported by the Arc2D class.

## Methods

| Name | Description |
|----|----|
| [classType](Arc2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Arc2D_copy.md) | Creates and returns an independent copy of this Arc2D object. |
| [createByCenter](Arc2D_createByCenter.md) | Creates a transient 2D arc object specifying the center, radius and start and end angles. A transient arc is not displayed or saved in a document. Transient arcs are used as a wrapper to work with raw 2D arc information. |
| [createByThreePoints](Arc2D_createByThreePoints.md) | Creates a transient 2D arc by specifying 3 points. A transient arc is not displayed or saved in a document. Transient arcs are used as a wrapper to work with raw 2D arc information. |
| [getData](Arc2D_getData.md) | Gets all of the data defining the arc. |
| [set](Arc2D_set.md) | Sets all of the data defining the arc. |
| [transformBy](Arc2D_transformBy.md) | Transforms this curve in 2D space. |

## Properties

| Name | Description |
| --- | --- |
| [asNurbsCurve](Arc2D_asNurbsCurve.md) | Returns a NURBS curve that is geometrically identical to the arc. |
| [center](Arc2D_center.md) | Gets and sets the center position of the arc. |
| [curveType](Arc2D_curveType.md) | Returns the type of geometry this curve represents. |
| [endAngle](Arc2D_endAngle.md) | Gets and sets the end angle of the arc in radians, where 0 is along the x axis. |
| [endPoint](Arc2D_endPoint.md) | Gets the position of the end point of the arc. |
| [evaluator](Arc2D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isClockwise](Arc2D_isClockwise.md) | Gets if the sweep direction of the arc is clockwise or counterclockwise. |
| [isValid](Arc2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Arc2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [radius](Arc2D_radius.md) | Gets and sets the radius of the arc. |
| [startAngle](Arc2D_startAngle.md) | Gets and sets the start angle of the arc in radians, where 0 is along the x axis. |
| [startPoint](Arc2D_startPoint.md) | Gets the position of the start point of the arc. |

## Accessed From

[Arc2D.copy](Arc2D_copy.md), [Arc2D.createByCenter](Arc2D_createByCenter.md), [Arc2D.createByThreePoints](Arc2D_createByThreePoints.md)

## Version

Introduced in version August 2014  

