# SplitFaceFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing split face features in a component and supports the ability to create new split face features.

## Methods

| Name | Description |
| --- | --- |
| [add](SplitFaceFeatures_add.md) | Creates a new split face feature. |
| [classType](SplitFaceFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](SplitFaceFeatures_createInput.md) | Creates a SplitFaceFeatureInput object. Use properties and methods on this object to define the split face you want to create and then use the Add method, passing in the SplitFaceFeatureInput object. A newly created SplitFaceFeatureInput object defaults to creating a split face feature using the "Split with Surface" option. You can use functions on the SplitFaceFeatureInput object to define a different type of split type. |
| [item](SplitFaceFeatures_item.md) | Function that returns the specified split face feature using an index into the collection. |
| [itemByName](SplitFaceFeatures_itemByName.md) | Function that returns the specified split face feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](SplitFaceFeatures_count.md) | The number of split face features in the collection. |
| [isValid](SplitFaceFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SplitFaceFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.splitFaceFeatures](Features_splitFaceFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Split Face Feature API Sample](SplitFaceFeatureSample_Sample.md) | Demonstrates creating a new split face feature. |

## Version

Introduced in version June 2015  

