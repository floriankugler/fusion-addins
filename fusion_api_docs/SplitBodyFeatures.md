# SplitBodyFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing split body features in a component and supports the ability to create new split body features.

## Methods

| Name | Description |
|----|----|
| [add](SplitBodyFeatures_add.md) | Creates a new split body feature. |
| [classType](SplitBodyFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](SplitBodyFeatures_createInput.md) | Creates a SplitBodyFeatureInput object. Use properties and methods on this object to define the split body you want to create and then use the Add method, passing in the SplitBodyFeatureInput object. |
| [item](SplitBodyFeatures_item.md) | Function that returns the specified split body feature using an index into the collection. |
| [itemByName](SplitBodyFeatures_itemByName.md) | Function that returns the specified split body feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](SplitBodyFeatures_count.md) | The number of split body features in the collection. |
| [isValid](SplitBodyFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SplitBodyFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.splitBodyFeatures](Features_splitBodyFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Split Body Feature API Sample](SplitBodyFeatureSample_Sample.md) | Demonstrates creating a new split body feature. |

## Version

Introduced in version June 2015  

