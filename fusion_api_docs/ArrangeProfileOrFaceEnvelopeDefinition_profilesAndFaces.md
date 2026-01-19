# ArrangeProfileOrFaceEnvelopeDefinition.profilesAndFaces Property

Parent Object: [ArrangeProfileOrFaceEnvelopeDefinition](ArrangeProfileOrFaceEnvelopeDefinition.md)  

## Description

Gets and sets an array containing any combination of Profile and planar BRepFace objects. These objects define the shapes of the envelopes. Currently, if a Profile is used, it must be the only Profile in its parent sketch.

## Syntax

"arrangeProfileOrFaceEnvelopeDefinition_var" is a variable referencing an ArrangeProfileOrFaceEnvelopeDefinition object.  

```python
# Get the value of the property.
propertyValue = arrangeProfileOrFaceEnvelopeDefinition_var.profilesAndFaces

# Set the value of the property.
arrangeProfileOrFaceEnvelopeDefinition_var.profilesAndFaces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [Base](Base.md).

## Version

Introduced in version January 2025  

