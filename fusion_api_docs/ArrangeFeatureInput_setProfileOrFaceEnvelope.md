# ArrangeFeatureInput.setProfileOrFaceEnvelope Method

Parent Object: [ArrangeFeatureInput](ArrangeFeatureInput.md)  

## Description

Defines an envelope defined by one or more profiles or planar faces. Only a single envelope input can exist at time. Calling this method will cause any existing envelope input object to be invalid.

## Syntax

"arrangeFeatureInput_var" is a variable referencing an [ArrangeFeatureInput](ArrangeFeatureInput.md) object.

```python
returnValue = arrangeFeatureInput_var.setProfileOrFaceEnvelope(profilesOrFaces)
```

## Return Value

| Type | Description |
|----|----|
| [Arrange2DProfileOrFaceEnvelopeInput](Arrange2DProfileOrFaceEnvelopeInput.md) | Returns the created Arrange2DProfileOrFaceEnvelopeInput object or null if the creation fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| profilesOrFaces | Base\[\] | An array of Profile and planar BRepFace objects that define the shape of the available envelopes. |

## Version

Introduced in version January 2025  

