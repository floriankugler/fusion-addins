
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

A collection of named values. The values are strings that Fusion stores but can be anything you choose. If you have several things you need to save you can choose to combine the data into a JSON or XML representation and save it as a single custom value or create a new custom value or each unique value you want to store. Fusion doesn't care what the value is or what it represents but only saves and provides access to it.

## Methods

| Name | Description |
|----|----|
| [addOrSetValue](CustomNamedValues_addOrSetValue.md) | Adds or updates a value. If the specified ID does not exist, a new named value is added. If the ID does exist, the named value is updated with the specified value. |
| [classType](CustomNamedValues_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [idByIndex](CustomNamedValues_idByIndex.md) | Function that returns the name of a value specified by its index. |
| [isExistingValue](CustomNamedValues_isExistingValue.md) | Function that returns if a value with the specified ID exists or not. |
| [remove](CustomNamedValues_remove.md) | Removes the specified value from the collection. |
| [value](CustomNamedValues_value.md) | Function that returns the specified value given its ID. |

## Properties

| Name | Description |
| --- | --- |
| [count](CustomNamedValues_count.md) | The number of values in the collection. |
| [isValid](CustomNamedValues_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CustomNamedValues_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CustomFeature.customNamedValues](CustomFeature_customNamedValues.md)

## Version

Introduced in version July 2021  

