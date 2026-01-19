# ExtendFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Extend features in a component and supports the ability to create new Extend features.

## Methods

| Name | Description |
|----|----|
| [add](ExtendFeatures_add.md) | Creates a new extend feature. |
| [classType](ExtendFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](ExtendFeatures_createInput.md) | Creates an ExtendFeatureInput object. Use properties and methods on this object to define the extend feature you want to create and then use the Add method, passing in the ExtendFeatureInput object. |
| [item](ExtendFeatures_item.md) | Function that returns the specified extend feature using an index into the collection. |
| [itemByName](ExtendFeatures_itemByName.md) | Function that returns the specified extend feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](ExtendFeatures_count.md) | The number of Extend features in the collection. |
| [isValid](ExtendFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ExtendFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.extendFeatures](Features_extendFeatures.md)

## Samples

| Name | Description |
|----|----|
| [extendFeatures.add](extendFeatures_add_Sample.md) | Demonstrates the extendFeatures.add method. To use this sample, have a design open that contains at least one surface body. When you run the sample, you will be prompted to select an open edge of the body. |
| [Extend Feature API Sample](ExtendFeatureSample_Sample.md) | Demonstrates creating a new extend feature. |

## Version

Introduced in version June 2015  

