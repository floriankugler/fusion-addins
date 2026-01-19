# FormFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Form features in a component.

## Methods

| Name | Description |
|----|----|
| [add](FormFeatures_add.md) | Creates a new empty form feature in the parent component. |
| [classType](FormFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](FormFeatures_item.md) | Function that returns the specified Form feature using an index into the collection. |
| [itemByName](FormFeatures_itemByName.md) | Function that returns the specified form feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](FormFeatures_count.md) | The number of Form features in the collection. |
| [isValid](FormFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](FormFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.formFeatures](Features_formFeatures.md)

## Version

Introduced in version September 2015  

