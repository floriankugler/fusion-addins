# ReverseNormalFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Reverse Normal features in a component and supports the ability to create new Reverse Normal features.

## Methods

| Name | Description |
|----|----|
| [add](ReverseNormalFeatures_add.md) | Creates a new Reverse Normal feature. |
| [classType](ReverseNormalFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ReverseNormalFeatures_item.md) | Function that returns the specified Reverse Normal feature using an index into the collection. |
| [itemByName](ReverseNormalFeatures_itemByName.md) | Function that returns the specified reverse normal feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](ReverseNormalFeatures_count.md) | The number of Reverse Normal features in the collection. |
| [isValid](ReverseNormalFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ReverseNormalFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.reverseNormalFeatures](Features_reverseNormalFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Reverse Normal Feature](ReverseNormalFeatureSample_Sample.md) | Demonstrates creating a new reverse normal feature. |

## Version

Introduced in version September 2015  

