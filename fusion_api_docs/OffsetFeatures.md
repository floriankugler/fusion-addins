# OffsetFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Offset features in a component and supports the ability to create new Offset features.

## Methods

| Name | Description |
|----|----|
| [add](OffsetFeatures_add.md) | Creates a new offset feature. |
| [classType](OffsetFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](OffsetFeatures_createInput.md) | Creates an OffsetFeatureInput object. Use properties and methods on this object to define the offset feature you want to create and then use the Add method, passing in the OffsetFeatureInput object to create the feature. |
| [item](OffsetFeatures_item.md) | Function that returns the specified offset feature using an index into the collection. |
| [itemByName](OffsetFeatures_itemByName.md) | Function that returns the specified offset feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](OffsetFeatures_count.md) | The number of Offset features in the collection. |
| [isValid](OffsetFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](OffsetFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.offsetFeatures](Features_offsetFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Offset Feature API Sample](OffsetFeatureSample_Sample.md) | Demonstrates creating a new offset feature |

## Version

Introduced in version June 2015  

