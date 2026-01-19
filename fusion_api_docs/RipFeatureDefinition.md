# RipFeatureDefinition Object

Derived from: [Base](Base.md) Object  

## Description

A Base class to return the information used to define the RipFeature.

## Methods

| Name | Description |
|----|----|
| [classType](RipFeatureDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](RipFeatureDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RipFeatureDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[RipFeature.definition](RipFeature_definition.md)

## Derived Classes

[AlongEdgeRipFeatureDefinition](AlongEdgeRipFeatureDefinition.md), [BetweenPointsRipFeatureDefinition](BetweenPointsRipFeatureDefinition.md), [FaceRipFeatureDefinition](FaceRipFeatureDefinition.md)

## Samples

| Name | Description |
|----|----|
| [Rip Feature Sample](RipFeatureSample_Sample.md) | Demonstrates creating a new sheet metal rip feature. |

## Version

Introduced in version September 2023  

