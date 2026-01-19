# SilhouetteSplitFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Silhouette Split features in a component and supports the ability to create new Silhouette Split features.

## Methods

| Name | Description |
|----|----|
| [add](SilhouetteSplitFeatures_add.md) | Creates a new silhouette split feature. |
| [classType](SilhouetteSplitFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](SilhouetteSplitFeatures_createInput.md) | Creates a SilhouetteSplitFeatureInput object. Use properties and methods on this object to define the silhouette split you want to create and then use the Add method, passing in the SilhouetteSplitFeatureInput object. |
| [item](SilhouetteSplitFeatures_item.md) | Function that returns the specified silhouette split feature using an index into the collection. |
| [itemByName](SilhouetteSplitFeatures_itemByName.md) | Function that returns the specified silhouette split feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](SilhouetteSplitFeatures_count.md) | The number of Silhouette Split features in the collection. |
| [isValid](SilhouetteSplitFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SilhouetteSplitFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.silhouetteSplitFeatures](Features_silhouetteSplitFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Silhouette Split Feature API Sample](SilhouetteSplitFeatureSample_Sample.md) | Demonstrates creating a new silhouette split feature. |

## Version

Introduced in version June 2015  

