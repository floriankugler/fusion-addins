# ThickenFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Thicken features in a component and supports the ability to create new Thicken features.

## Methods

| Name | Description |
|----|----|
| [add](ThickenFeatures_add.md) | Creates a new Thicken feature. |
| [classType](ThickenFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](ThickenFeatures_createInput.md) | Creates a ThickenFeatureInput object. Use properties and methods on this object to define the Thicken feature you want to create and then use the Add method, passing in the ThickenFeatureInput object to create the feature. |
| [item](ThickenFeatures_item.md) | Function that returns the specified Thicken feature using an index into the collection. |
| [itemByName](ThickenFeatures_itemByName.md) | Function that returns the specified thicken feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](ThickenFeatures_count.md) | The number of Thicken features in the collection. |
| [isValid](ThickenFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ThickenFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.thickenFeatures](Features_thickenFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Thicken Feature API Sample](ThickenFeatureSample_Sample.md) | Demonstrates creating a new thiken feature. |

## Version

Introduced in version June 2015  

