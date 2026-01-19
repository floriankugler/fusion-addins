# FlangeFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing flange features in a design.

## Methods

| Name | Description |
|----|----|
| [classType](FlangeFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](FlangeFeatures_item.md) | Function that returns the specified flange feature using an index into the collection. |
| [itemByName](FlangeFeatures_itemByName.md) | Function that returns the specified flange feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](FlangeFeatures_count.md) | The number of flange features in the collection. |
| [isValid](FlangeFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](FlangeFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.flangeFeatures](Features_flangeFeatures.md)

## Version

Introduced in version August 2020  

