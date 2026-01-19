# TrimFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing trim features in a component and supports the ability to create new trim features.

## Methods

| Name | Description |
| --- | --- |
| [add](TrimFeatures_add.md) | Creates a new trim feature. |
| [classType](TrimFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](TrimFeatures_createInput.md) | Creates a TrimFeatureInput object. Use properties and methods on this object to define the trim feature you want to create and then use the Add method, passing in the TrimFeatureInput object. To determine the possible boundaries and allow you to choose which cells to keep, the trim feature does a partial compute when the input object is created. To do this it starts a trim feature transaction and completes the transaction when you call the add method. If you don't call the add method to finish the transaction it leaves Fusion in a bad state and there will be undo problems and possibly a crash. If you have created a TrimFeatureInput object and don't want to finish the feature creation, you need to call the cancel method on the TrimFeatureInput object to safely abort the current boundary fill transaction. |
| [item](TrimFeatures_item.md) | Function that returns the specified trim feature using an index into the collection. |
| [itemByName](TrimFeatures_itemByName.md) | Function that returns the specified trim feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](TrimFeatures_count.md) | The number of trim features in the collection. |
| [isValid](TrimFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](TrimFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.trimFeatures](Features_trimFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Trim Feature API Sample](TrimFeatureSample_Sample.md) | Demonstrates creating a new trim feature. |

## Version

Introduced in version July 2015  

