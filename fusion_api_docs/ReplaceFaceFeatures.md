# ReplaceFaceFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing replace face features in a component and supports the ability to create new replace face features.

## Methods

| Name | Description |
|----|----|
| [add](ReplaceFaceFeatures_add.md) | Creates a new replace face feature. |
| [classType](ReplaceFaceFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](ReplaceFaceFeatures_createInput.md) | Creates a ReplaceFaceFeatureInput object. Use properties and methods on this object to define the replace face you want to create and then use the Add method, passing in the ReplaceFaceFeatureInput object. |
| [item](ReplaceFaceFeatures_item.md) | Function that returns the specified replace face feature using an index into the collection. |
| [itemByName](ReplaceFaceFeatures_itemByName.md) | Function that returns the specified replace face feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](ReplaceFaceFeatures_count.md) | The number of replace face features in the collection. |
| [isValid](ReplaceFaceFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ReplaceFaceFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.replaceFaceFeatures](Features_replaceFaceFeatures.md)

## Samples

| Name | Description |
|----|----|
| [ReplaceFace Feature](ReplaceFaceFeatureSample_Sample.md) | Demonstrates creating a new replaceface feature. |

## Version

Introduced in version March 2015  

