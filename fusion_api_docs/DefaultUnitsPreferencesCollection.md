# DefaultUnitsPreferencesCollection Object

Derived from: [Base](Base.md) Object  

## Description

A collection that provides access to product specific unit preference objects.

## Methods

| Name | Description |
|----|----|
| [classType](DefaultUnitsPreferencesCollection_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](DefaultUnitsPreferencesCollection_item.md) | Function that returns the specified DefaultUnitPreferences object using an index into the collection. |
| [itemByName](DefaultUnitsPreferencesCollection_itemByName.md) | Returns the DefaultUnitsPreference object with the specified name. |

## Properties

| Name | Description |
| --- | --- |
| [count](DefaultUnitsPreferencesCollection_count.md) | Returns the number of DefaultUnitsPreference objects. |
| [isValid](DefaultUnitsPreferencesCollection_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DefaultUnitsPreferencesCollection_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Preferences.defaultUnitsPreferences](Preferences_defaultUnitsPreferences.md)

## Version

Introduced in version August 2014  

