# UnstitchFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Unstitch features in a component and supports the ability to create new Unstitch features.

## Methods

| Name | Description |
|----|----|
| [add](UnstitchFeatures_add.md) | Creates a new Unstitch feature. |
| [classType](UnstitchFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](UnstitchFeatures_item.md) | Function that returns the specified Unstitch feature using an index into the collection. |
| [itemByName](UnstitchFeatures_itemByName.md) | Function that returns the specified unstitch feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](UnstitchFeatures_count.md) | The number of Unstitch features in the collection. |
| [isValid](UnstitchFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](UnstitchFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.unstitchFeatures](Features_unstitchFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Unstitch Feature API Sample](UnstitchFeatureSample_Sample.md) | Demonstrates creating a new unstitch feature |

## Version

Introduced in version July 2015  

