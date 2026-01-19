# NamedValues Object

Derived from: [Base](Base.md) Object  

## Description

Wraps a list of named values.

## Methods

| Name | Description |
|----|----|
| [add](NamedValues_add.md) | Adds a name value pair to the NamedValues object |
| [classType](NamedValues_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](NamedValues_create.md) | Creates a transient NamedValues object. |
| [getByIndex](NamedValues_getByIndex.md) | Function that returns the name and ValueInput object of a name value pair by specifying an index number |
| [getValueByName](NamedValues_getValueByName.md) | Function that returns the ValueInput object of a name value pair by specifying its name |

## Properties

| Name | Description |
| --- | --- |
| [count](NamedValues_count.md) | Returns the number of name value pairs in this object. |
| [isValid](NamedValues_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](NamedValues_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[NamedValues.create](NamedValues_create.md), [PostProcessInput.postProperties](PostProcessInput_postProperties.md), [ToolQuery.criteria](ToolQuery_criteria.md)

## Version

Introduced in version August 2014  

