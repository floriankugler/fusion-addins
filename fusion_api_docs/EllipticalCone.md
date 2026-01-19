# EllipticalCone Object

Derived from: [Surface](Surface.md) Object  

## Description

Transient elliptical cone. A transient elliptical cone is not displayed or saved in a document. A transient elliptical cone is used as a wrapper to work with raw elliptical cone information. A transient elliptical cone has no boundaries. The cone always goes to a point in its narrowing direction, and is infinite in its widening direction. They are created statically using the create method of the EllipticalCone class.

## Methods

| Name | Description |
|----|----|
| [classType](EllipticalCone_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](EllipticalCone_copy.md) | Creates and returns an independent copy of this EllipticalCone object. |
| [create](EllipticalCone_create.md) | Creates a transient elliptical cone object. |
| [getAxes](EllipticalCone_getAxes.md) | Gets the center axis of the cone that defines its normal direction and the major axis direction of the ellipse that defines it. |
| [getData](EllipticalCone_getData.md) | Gets the data that defines the Elliptical Cone. |
| [set](EllipticalCone_set.md) | Sets the data that defines the Elliptical Cone. |
| [setAxes](EllipticalCone_setAxes.md) | Sets the center axis of the cone and the major axis direction of the ellipse that defines it. |
| [transformBy](EllipticalCone_transformBy.md) | Updates this surface by transforming it with a given input matrix. |

## Properties

| Name | Description |
| --- | --- |
| [evaluator](EllipticalCone_evaluator.md) | Returns the surface evaluator. |
| [halfAngle](EllipticalCone_halfAngle.md) | Gets and sets the taper half-angle of the elliptical cone. A negative value indicates that the cone is narrowing in the direction of the axis vector, whereas a positive values indicates that it is expanding in the direction of the axis vector. |
| [isValid](EllipticalCone_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [majorRadius](EllipticalCone_majorRadius.md) | Gets and sets the major radius of the ellipse that defines the cone. |
| [minorRadius](EllipticalCone_minorRadius.md) | Gets and sets the minor radius of the ellipse that defines the cone. |
| [objectType](EllipticalCone_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [origin](EllipticalCone_origin.md) | Gets and sets the origin point (center) of the base of the cone. |
| [surfaceType](EllipticalCone_surfaceType.md) | Returns the surface type. |

## Accessed From

[EllipticalCone.copy](EllipticalCone_copy.md), [EllipticalCone.create](EllipticalCone_create.md)

## Version

Introduced in version August 2014  

