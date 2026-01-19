# RipFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a Rip feature.

## Methods

| Name | Description |
|----|----|
| [classType](RipFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setAlongEdge](RipFeatureInput_setAlongEdge.md) | Specifies the rip feature will be along an edge. |
| [setBetweenPoints](RipFeatureInput_setBetweenPoints.md) | This input method is for creating a rip between two points. Each point can be either a BRepVertex or a BRepEdge and an associated offset along the edge. |
| [setByFace](RipFeatureInput_setByFace.md) | Specifies the rip feature will be defined by a face.. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](RipFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RipFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[RipFeatures.createRipFeatureInput](RipFeatures_createRipFeatureInput.md)

## Samples

| Name | Description |
|----|----|
| [Rip Feature Sample](RipFeatureSample_Sample.md) | Demonstrates creating a new sheet metal rip feature. |

## Version

Introduced in version September 2023  

