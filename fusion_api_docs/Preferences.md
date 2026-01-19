# Preferences Object

Derived from: [Base](Base.md) Object  

## Description

The Preferences object provides access to the various preference related objects for getting and setting the various preference values.

## Methods

| Name | Description |
|----|----|
| [classType](Preferences_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [apiPreferences](Preferences_apiPreferences.md) | Gets the APIPreferences object, which provides access to the various preferences associated with the API. |
| [defaultUnitsPreferences](Preferences_defaultUnitsPreferences.md) | Gets the DefaultUnitsPreferences object. |
| [generalPreferences](Preferences_generalPreferences.md) | Gets the GeneralPreferences object. |
| [graphicsPreferences](Preferences_graphicsPreferences.md) | Gets the GraphicsPreferences object. |
| [gridPreferences](Preferences_gridPreferences.md) | Gets the GridPreferences object. |
| [isValid](Preferences_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [materialPreferences](Preferences_materialPreferences.md) | Gets the MaterialPreferences object. |
| [networkPreferences](Preferences_networkPreferences.md) | Gets the NetworkPreferences object. |
| [objectType](Preferences_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [productPreferences](Preferences_productPreferences.md) | Gets the ProductPreferences object. |
| [productUsageData](Preferences_productUsageData.md) | Gets the ProductUsageData object. |
| [unitAndValuePreferences](Preferences_unitAndValuePreferences.md) | Gets the UnitAndValuePreferences object. |

## Accessed From

[Application.preferences](Application_preferences.md)

## Version

Introduced in version August 2014  

