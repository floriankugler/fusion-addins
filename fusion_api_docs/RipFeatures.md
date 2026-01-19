# RipFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Rip features in a design.

## Methods

| Name | Description |
|----|----|
| [add](RipFeatures_add.md) | Creates a new Rip feature. |
| [classType](RipFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createRipFeatureInput](RipFeatures_createRipFeatureInput.md) | Creates a RipFeatureInput object. Use methods on this object to define the rip you want to create and then use the add method, passing in the RipFeatureInput object. |
| [item](RipFeatures_item.md) | Function that returns the specified Rip feature using an index into the collection. |
| [itemByName](RipFeatures_itemByName.md) | Function that returns the specified Rip feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](RipFeatures_count.md) | The number of Rip features in the collection. |
| [isValid](RipFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RipFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.ripFeatures](Features_ripFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Rip Feature Sample](RipFeatureSample_Sample.md) | Demonstrates creating a new sheet metal rip feature. |

## Version

Introduced in version September 2023  

