# RecognizedHoles Object

Derived from: [Base](Base.md) Object  

## Description

Object that represents a collection of holes.

## Methods

| Name | Description |
|----|----|
| [classType](RecognizedHoles_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](RecognizedHoles_item.md) | Returns the hole at the specified index from this collection of holes. |

## Properties

| Name | Description |
| --- | --- |
| [count](RecognizedHoles_count.md) | Returns the number of holes contained in this hole collection. |
| [isValid](RecognizedHoles_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RecognizedHoles_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[RecognizedHole.recognizeHoles](RecognizedHole_recognizeHoles.md), [RecognizedHole.recognizeHolesWithInput](RecognizedHole_recognizeHolesWithInput.md)

## Version

Introduced in version May 2023  

