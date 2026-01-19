# Torus Object

Derived from: [Surface](Surface.md) Object  

## Description

Transient torus. A transient torus is not displayed or saved in a document. A transient torus is used as a wrapper to work with raw torus information. A transient torus is a full torus with no boundaries. They are created statically using the create method of the Torus class.

## Methods

| Name | Description |
|----|----|
| [classType](Torus_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Torus_copy.md) | Creates and returns an independent copy of this Torus object. |
| [create](Torus_create.md) | Creates a transient torus object. |
| [getData](Torus_getData.md) | Gets all of the data defining the torus. |
| [set](Torus_set.md) | Sets all of the data defining the torus. |
| [transformBy](Torus_transformBy.md) | Updates this surface by transforming it with a given input matrix. |

## Properties

| Name | Description |
| --- | --- |
| [axis](Torus_axis.md) | Gets and sets the center axis of the torus. |
| [evaluator](Torus_evaluator.md) | Returns the surface evaluator. |
| [isValid](Torus_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [majorRadius](Torus_majorRadius.md) | Gets and sets the major radius of the torus. |
| [minorRadius](Torus_minorRadius.md) | Gets and sets the minor radius of the torus. |
| [objectType](Torus_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [origin](Torus_origin.md) | Gets and sets the origin point (center) of the torus. |
| [surfaceType](Torus_surfaceType.md) | Returns the surface type. |

## Accessed From

[Torus.copy](Torus_copy.md), [Torus.create](Torus_create.md)

## Version

Introduced in version August 2014  

