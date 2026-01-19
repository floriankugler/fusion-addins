# Cone Object

Derived from: [Surface](Surface.md) Object  

## Description

Transient cone. A transient cone is not displayed or saved in a document. A transient cone is used as a wrapper to work with raw cone information. A transient cone has no boundaries. The cone always goes to a point in its narrowing direction, and is infinite in its widening direction. They are created statically using the create method of the Cone class.

## Methods

| Name | Description |
|----|----|
| [classType](Cone_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Cone_copy.md) | Creates and returns an independent copy of this Cone object. |
| [create](Cone_create.md) | Creates a transient cone object. |
| [getData](Cone_getData.md) | Gets the data that defines the cone. |
| [set](Cone_set.md) | Sets the data that defines the cone. |
| [transformBy](Cone_transformBy.md) | Updates this surface by transforming it with a given input matrix. |

## Properties

| Name | Description |
| --- | --- |
| [axis](Cone_axis.md) | Gets and sets the center axis (along the length) of the cone that defines its normal direction. |
| [evaluator](Cone_evaluator.md) | Returns the surface evaluator. |
| [halfAngle](Cone_halfAngle.md) | Gets and sets the taper half-angle of the cone in radians. A negative value indicates that the cone is narrowing in the direction of the axis vector, whereas a positive value indicates that it is expanding in the direction of the axis vector. |
| [isValid](Cone_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Cone_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [origin](Cone_origin.md) | Gets and sets the origin point (center) of the base of the cone. |
| [radius](Cone_radius.md) | Gets and sets the radius of the cone. |
| [surfaceType](Cone_surfaceType.md) | Returns the surface type. |

## Accessed From

[Cone.copy](Cone_copy.md), [Cone.create](Cone_create.md)

## Version

Introduced in version August 2014  

