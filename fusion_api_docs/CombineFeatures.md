# CombineFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Combine features in a component and supports the ability to create new Combine features.

## Methods

| Name | Description |
|----|----|
| [add](CombineFeatures_add.md) | Creates a new combine feature. |
| [classType](CombineFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](CombineFeatures_createInput.md) | Creates a CombineFeatureInput object. Use properties and methods on this object to define the combine you want to create and then use the Add method, passing in the CombineFeatureInput object. |
| [item](CombineFeatures_item.md) | Function that returns the specified combine feature using an index into the collection. |
| [itemByName](CombineFeatures_itemByName.md) | Function that returns the specified combine feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](CombineFeatures_count.md) | The number of combine features in the collection. This property returns nothing in the case where the feature is non-parametric. |
| [isValid](CombineFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CombineFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.combineFeatures](Features_combineFeatures.md)

## Version

Introduced in version November 2014  

