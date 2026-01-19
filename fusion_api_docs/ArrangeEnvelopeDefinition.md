# ArrangeEnvelopeDefinition Object

Derived from: [Base](Base.md) Object  

## Description

The ArrangeEnvelope object is the base class for the different types of arrangement envelopes and provides access to the information that defines the envelope(s). This defines the settings of the envelope and the EnvelopeResult provides access to the resulting envelope and its contents.

## Methods

| Name | Description |
|----|----|
| [classType](ArrangeEnvelopeDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [frameWidth](ArrangeEnvelopeDefinition_frameWidth.md) | Returns the parameter that controls the width of the envelope frame. This defines the offset distance of the objects from the edge of the frame. You can modify the value by using the properties on the returned ModelParameter object. |
| [isPartialArrangeAllowed](ArrangeEnvelopeDefinition_isPartialArrangeAllowed.md) | Gets and sets if a partial arrange is allowed for this envelope. |
| [isValid](ArrangeEnvelopeDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectSpacing](ArrangeEnvelopeDefinition_objectSpacing.md) | Returns the parameter that controls the space between objects in the arrangement. You can modify the value by using the properties on the returned ModelParameter object. |
| [objectType](ArrangeEnvelopeDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentArrange](ArrangeEnvelopeDefinition_parentArrange.md) | Returns the parent ArrangeFeature this envelope is associated with. |
| [placementClearance](ArrangeEnvelopeDefinition_placementClearance.md) | Returns the parameter that controls the offset of the objects from the base plane of the arrangement (the "up" direction). You can modify the value by using the properties on the returned ModelParameter object. |

## Accessed From

[Arrange3DResultEnvelope.envelopeDefinition](Arrange3DResultEnvelope_envelopeDefinition.md), [ArrangeFeature.envelopeDefinition](ArrangeFeature_envelopeDefinition.md), [ArrangePlaneResultEnvelope.envelopeDefinition](ArrangePlaneResultEnvelope_envelopeDefinition.md), [ArrangeProfileOrFaceResultEnvelope.envelopeDefinition](ArrangeProfileOrFaceResultEnvelope_envelopeDefinition.md), [ArrangeResultEnvelope.envelopeDefinition](ArrangeResultEnvelope_envelopeDefinition.md)

## Derived Classes

[Arrange3DEnvelopeDefinition](Arrange3DEnvelopeDefinition.md), [ArrangePlaneEnvelopeDefinition](ArrangePlaneEnvelopeDefinition.md), [ArrangeProfileOrFaceEnvelopeDefinition](ArrangeProfileOrFaceEnvelopeDefinition.md)

## Version

Introduced in version January 2025  

