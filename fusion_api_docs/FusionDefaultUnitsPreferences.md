# FusionDefaultUnitsPreferences Object

Derived from: [DefaultUnitsPreferences](DefaultUnitsPreferences.md) Object  

## Description

Fusion Default Units for Design Preferences. The following code can be used to access this object.

```python
unitPrefs = app.preferences.defaultUnitsPreferences.itemByName('Design')
```

## Methods

| Name | Description |
|----|----|
| [classType](FusionDefaultUnitsPreferences_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [defaultUnitSystem](FusionDefaultUnitsPreferences_defaultUnitSystem.md) | Gets and sets the default unit system when creating a new Fusion file. |
| [distanceDisplayUnits](FusionDefaultUnitsPreferences_distanceDisplayUnits.md) | Gets and sets the default design units for length when creating a new Fusion file. Setting this property will have the side effect of changing the defaultUnitSystem property to custom. |
| [isValid](FusionDefaultUnitsPreferences_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [massDisplayUnits](FusionDefaultUnitsPreferences_massDisplayUnits.md) | Gets and sets the default design units for mass when creating a new Fusion file. Setting this property will have the side effect of changing the defaultUnitSystem property to custom. |
| [name](FusionDefaultUnitsPreferences_name.md) | Returns the name of this DefaultUnitPreferences object. |
| [objectType](FusionDefaultUnitsPreferences_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Version

Introduced in version August 2014  

