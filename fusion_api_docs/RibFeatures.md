# RibFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing rib features in a design.

## Methods

| Name | Description |
|----|----|
| [classType](RibFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](RibFeatures_item.md) | Function that returns the specified Rib feature using an index into the collection. |
| [itemByName](RibFeatures_itemByName.md) | Function that returns the specified Rib feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](RibFeatures_count.md) | The number of Rib features in the collection. |
| [isValid](RibFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RibFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.ribFeatures](Features_ribFeatures.md)

## Version

Introduced in version September 2015  

