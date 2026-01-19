# EllipticalCylinder Object

Derived from: [Surface](Surface.md) Object  

## Description

Transient elliptical cylinder. A transient elliptical cylinder is not displayed or saved in a document. A transient elliptical cylinder is used as a wrapper to work with raw elliptical cylinder information. A transient elliptical cylinder has no boundaries and is infinite in length. They are created statically using the create method of the EllipticalCylinder class.

## Methods

| Name | Description |
|----|----|
| [classType](EllipticalCylinder_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](EllipticalCylinder_copy.md) | Creates and returns an independent copy of this EllipticalCylinder object. |
| [create](EllipticalCylinder_create.md) | Creates a transient 3D elliptical cylinder object. |
| [getData](EllipticalCylinder_getData.md) | Gets the data defining the elliptical cylinder. |
| [set](EllipticalCylinder_set.md) | Sets the data defining the elliptical cylinder. |
| [transformBy](EllipticalCylinder_transformBy.md) | Updates this surface by transforming it with a given input matrix. |

## Properties

| Name | Description |
| --- | --- |
| [axis](EllipticalCylinder_axis.md) | Gets and set the center axis (along the length) of the cylinder that defines its normal direction. |
| [evaluator](EllipticalCylinder_evaluator.md) | Returns the surface evaluator. |
| [isValid](EllipticalCylinder_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [majorAxis](EllipticalCylinder_majorAxis.md) | Gets and sets the direction of the major axis of the ellipse that defines the cylinder. |
| [majorRadius](EllipticalCylinder_majorRadius.md) | Gets and sets the major radius of the ellipse that defines the cylinder. |
| [minorRadius](EllipticalCylinder_minorRadius.md) | Gets and sets the minor radius of the ellipse that defines the cylinder. |
| [objectType](EllipticalCylinder_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [origin](EllipticalCylinder_origin.md) | Gets and sets the origin point (center) of the base of the cylinder. |
| [surfaceType](EllipticalCylinder_surfaceType.md) | Returns the surface type. |

## Accessed From

[EllipticalCylinder.copy](EllipticalCylinder_copy.md), [EllipticalCylinder.create](EllipticalCylinder_create.md)

## Version

Introduced in version August 2014  

