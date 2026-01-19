# ProductPreferences Object

Derived from: [Base](Base.md) Object  

## Description

The base class for the general product preferences. There is a derived class for each product where the specific preference values are exposed.

## Methods

| Name | Description |
|----|----|
| [classType](ProductPreferences_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ProductPreferences_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ProductPreferences_name.md) | Returns the name of this ProductPreferences object. |
| [objectType](ProductPreferences_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ProductPreferencesCollection.item](ProductPreferencesCollection_item.md), [ProductPreferencesCollection.itemByName](ProductPreferencesCollection_itemByName.md)

## Derived Classes

[FusionProductPreferences](FusionProductPreferences.md)

## Version

Introduced in version August 2014  

