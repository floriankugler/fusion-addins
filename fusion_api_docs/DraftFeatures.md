# DraftFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing draft features in a component and supports the ability to create new draft features.

## Methods

| Name | Description |
|----|----|
| [add](DraftFeatures_add.md) | Creates a new draft feature. |
| [classType](DraftFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](DraftFeatures_createInput.md) | Creates a DraftFeatureInput object. Use properties and methods on this object to define the draft you want to create and then use the Add method, passing in the DraftFeatureInput object. |
| [item](DraftFeatures_item.md) | Function that returns the specified draft feature using an index into the collection. |
| [itemByName](DraftFeatures_itemByName.md) | Function that returns the specified draft feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](DraftFeatures_count.md) | The number of draft features in the collection. |
| [isValid](DraftFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DraftFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.draftFeatures](Features_draftFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Draft Feature API Sample](DraftFeatureSample_Sample.md) | Demonstrates creating a new draft feature. |

## Version

Introduced in version January 2015  

