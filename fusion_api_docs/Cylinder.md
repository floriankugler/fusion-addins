# Cylinder Object

Derived from: [Surface](Surface.md) Object  

## Description

Transient cylinder. A transient cylinder is not displayed or saved in a document. A transient cylinder is but is used as a wrapper to work with raw cylinder information. A transient cylinder has no boundaries and is infinite in length. They are created statically using the create method of the Cylinder class.

## Methods

| Name | Description |
|----|----|
| [classType](Cylinder_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Cylinder_copy.md) | Creates and returns an independent copy of this Cylinder object. |
| [create](Cylinder_create.md) | Creates a transient cylinder object. |
| [getData](Cylinder_getData.md) | Gets the data that defines the cylinder. |
| [set](Cylinder_set.md) | Sets the data that defines the cylinder. |
| [transformBy](Cylinder_transformBy.md) | Updates this surface by transforming it with a given input matrix. |

## Properties

| Name | Description |
| --- | --- |
| [axis](Cylinder_axis.md) | The center axis (along the length) of the cylinder that defines its normal direction. |
| [evaluator](Cylinder_evaluator.md) | Returns the surface evaluator. |
| [isValid](Cylinder_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Cylinder_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [origin](Cylinder_origin.md) | The origin point (center) of the base of the cylinder. |
| [radius](Cylinder_radius.md) | The radius of the cylinder. |
| [surfaceType](Cylinder_surfaceType.md) | Returns the surface type. |

## Accessed From

[Cylinder.copy](Cylinder_copy.md), [Cylinder.create](Cylinder_create.md)

## Version

Introduced in version August 2014  

