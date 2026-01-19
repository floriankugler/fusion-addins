# Profiles Object

Derived from: [Base](Base.md) Object  

## Description

A collection of all of the closed profiles currently calculated for this sketch. Closed profiles are automatically computed by Fusion and represent closed areas within the sketch.  

This class also provides some additional utility functions to create open profiles and text based profiles that can be used as input for various features.

## Methods

| Name | Description |
|----|----|
| [classType](Profiles_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](Profiles_item.md) | Function that returns the specified closed profile using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](Profiles_count.md) | Returns the number of closed profiles in the sketch. Open and text based profiles are not included. |
| [isValid](Profiles_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Profiles_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Sketch.profiles](Sketch_profiles.md)

## Samples

| Name | Description |
|----|----|
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |

## Version

Introduced in version August 2014  

