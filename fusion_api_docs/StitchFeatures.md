# StitchFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Stitch features in a component and supports the ability to create new Stitch features.

## Methods

| Name | Description |
|----|----|
| [add](StitchFeatures_add.md) | Creates a new stitch feature. |
| [classType](StitchFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](StitchFeatures_createInput.md) | Creates a StitchFeatureInput object. Use properties and methods on this object to define the stitch feature you want to create and then use the Add method, passing in the StitchFeatureInput object. |
| [item](StitchFeatures_item.md) | Function that returns the specified stitch feature using an index into the collection. |
| [itemByName](StitchFeatures_itemByName.md) | Function that returns the specified stitch feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](StitchFeatures_count.md) | The number of Stitch features in the collection. |
| [isValid](StitchFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](StitchFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.stitchFeatures](Features_stitchFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Stitch Feature API Sample](StitchFeatureSample_Sample.md) | Demonstrates creating a new stitch feature. |

## Version

Introduced in version June 2015  

