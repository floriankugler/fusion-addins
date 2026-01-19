# ArrangeResultEnvelopes Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the results of an arrangement. For 3D arrangements, this will always contain a single result. For plane or profile envelopes this can contain multiple envelope results.

## Methods

| Name | Description |
|----|----|
| [classType](ArrangeResultEnvelopes_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ArrangeResultEnvelopes_item.md) | Returns the specified Arrange envelope result using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](ArrangeResultEnvelopes_count.md) | Returns the number of Arrange envelope results for this Arrange feature. |
| [isValid](ArrangeResultEnvelopes_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ArrangeResultEnvelopes_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ArrangeFeature.resultEnvelopes](ArrangeFeature_resultEnvelopes.md)

## Version

Introduced in version January 2025  

