# ArrangeOccurrenceResults Object

Derived from: [Base](Base.md) Object  

## Description

A collection that contains the occurrences in an Arrange envelope.

## Methods

| Name | Description |
|----|----|
| [classType](ArrangeOccurrenceResults_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ArrangeOccurrenceResults_item.md) | Returns the specified Arrange occurrence using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](ArrangeOccurrenceResults_count.md) | Returns the number of Arrange occurrences in the collection. |
| [isValid](ArrangeOccurrenceResults_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ArrangeOccurrenceResults_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Arrange3DResultEnvelope.occurrences](Arrange3DResultEnvelope_occurrences.md), [ArrangePlaneResultEnvelope.occurrences](ArrangePlaneResultEnvelope_occurrences.md), [ArrangeProfileOrFaceResultEnvelope.occurrences](ArrangeProfileOrFaceResultEnvelope_occurrences.md), [ArrangeResultEnvelope.occurrences](ArrangeResultEnvelope_occurrences.md)

## Version

Introduced in version January 2025  

