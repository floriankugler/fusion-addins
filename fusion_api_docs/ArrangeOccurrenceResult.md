# ArrangeOccurrenceResult Object

Derived from: [Base](Base.md) Object  

## Description

The ArrangeOccurrence object represents a single occurrence within an Arrange envelope.

## Methods

| Name | Description |
|----|----|
| [classType](ArrangeOccurrenceResult_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [arrangeComponent](ArrangeOccurrenceResult_arrangeComponent.md) | The ArrangeComponent from the Arrange definition that resulted in the create of this occurrence. |
| [isValid](ArrangeOccurrenceResult_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ArrangeOccurrenceResult_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurrence](ArrangeOccurrenceResult_occurrence.md) | The Occurrence object in the Arrange envelope. |
| [parentEnvelope](ArrangeOccurrenceResult_parentEnvelope.md) | The Arrange envelope this occurrence is within. |

## Accessed From

[ArrangeOccurrenceResults.item](ArrangeOccurrenceResults_item.md)

## Version

Introduced in version January 2025  

