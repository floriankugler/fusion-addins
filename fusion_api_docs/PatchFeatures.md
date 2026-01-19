# PatchFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Patch features in a component and supports the ability to create new Patch features.

## Methods

| Name | Description |
|----|----|
| [add](PatchFeatures_add.md) | Creates a new patch feature. |
| [classType](PatchFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](PatchFeatures_createInput.md) | Creates a PatchFeatureInput object. Use properties and methods on the returned PatchFeatureInput object to set other settings. The PatchFeatureInput object is used as input to the add method to create the patch feature. |
| [item](PatchFeatures_item.md) | Function that returns the specified patch feature using an index into the collection. |
| [itemByName](PatchFeatures_itemByName.md) | Function that returns the specified patch feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](PatchFeatures_count.md) | The number of Patch features in the collection. |
| [isValid](PatchFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PatchFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.patchFeatures](Features_patchFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version September 2015  

