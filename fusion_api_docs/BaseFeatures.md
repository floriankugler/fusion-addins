# BaseFeatures Object

Derived from: [Base](Base.md) Object  

## Description

The BaseFeature class represents a direct edit feature within a parametric design.

## Methods

| Name | Description |
|----|----|
| [add](BaseFeatures_add.md) | Creates a new empty base feature in the parent component. |
| [classType](BaseFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](BaseFeatures_item.md) | Function that returns the specified base feature using an index into the collection. |
| [itemByName](BaseFeatures_itemByName.md) | Function that returns the specified base feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](BaseFeatures_count.md) | The number of base features in the collection. |
| [isValid](BaseFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BaseFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.baseFeatures](Features_baseFeatures.md)

## Samples

| Name | Description |
|----|----|
| [BaseFeature Sample](BaseFeatureSample_Sample.md) | Creates a new base feature. |

## Version

Introduced in version September 2015  

