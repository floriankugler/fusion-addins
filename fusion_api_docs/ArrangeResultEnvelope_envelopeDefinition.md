# ArrangeResultEnvelope.envelopeDefinition Property

Parent Object: [ArrangeResultEnvelope](ArrangeResultEnvelope.md)  

## Description

Returns the envelope definition that provides the settings for this envelope.  

To use this property, you need to position the timeline marker immediately before the Arrange feature. This can be accomplished using the following code: arrangeFeature.timelineObject.rollTo(True)

## Syntax

"arrangeResultEnvelope_var" is a variable referencing an ArrangeResultEnvelope object.  

```python
# Get the value of the property.
propertyValue = arrangeResultEnvelope_var.envelopeDefinition
```

## Property Value

This is a read only property whose value is an [ArrangeEnvelopeDefinition](ArrangeEnvelopeDefinition.md).

## Version

Introduced in version January 2025  

