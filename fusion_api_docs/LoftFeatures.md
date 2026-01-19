# LoftFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing loft features in a design.

## Methods

| Name | Description |
|----|----|
| [add](LoftFeatures_add.md) | Creates a new loft feature. |
| [classType](LoftFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](LoftFeatures_createInput.md) | Creates a LoftFeatureInput object. Use properties and methods on the returned LoftFeatureInput object to provide the required input to create a loft feature. The LoftFeatureInput object can then be used as input to the add method to create the loft feature. |
| [item](LoftFeatures_item.md) | Function that returns the specified loft feature using an index into the collection. |
| [itemByName](LoftFeatures_itemByName.md) | Function that returns the specified loft feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](LoftFeatures_count.md) | The number of loft features in the collection. |
| [isValid](LoftFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](LoftFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.loftFeatures](Features_loftFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version September 2015  

