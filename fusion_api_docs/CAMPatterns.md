# CAMPatterns Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to the patterns within an existing setup, folder or pattern.

## Methods

| Name | Description |
|----|----|
| [classType](CAMPatterns_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](CAMPatterns_item.md) | Function that returns the specified pattern using an index into the collection. |
| [itemByName](CAMPatterns_itemByName.md) | Returns the pattern with the specified name (as appears in the browser). |
| [itemByOperationId](CAMPatterns_itemByOperationId.md) | Returns the pattern with the specified operation id. |

## Properties

| Name | Description |
| --- | --- |
| [count](CAMPatterns_count.md) | The number of items in the collection. |
| [isValid](CAMPatterns_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CAMPatterns_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAMFolder.patterns](CAMFolder_patterns.md), [CAMPattern.patterns](CAMPattern_patterns.md), [Setup.patterns](Setup_patterns.md)

## Version

Introduced in version January 2016  

