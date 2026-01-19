# ArrangeFeature.envelopeDefinition Property

Parent Object: [ArrangeFeature](ArrangeFeature.md)  

## Description

Returns the envelope definition associated with this arrangement.  

To use this property, you need to position the timeline marker immediately before the Arrange feature. This can be accomplished using the following code: arrangeFeature.timelineObject.rollTo(True)

## Syntax

"arrangeFeature_var" is a variable referencing an ArrangeFeature object.  

```python
# Get the value of the property.
propertyValue = arrangeFeature_var.envelopeDefinition
```

## Property Value

This is a read only property whose value is an [ArrangeEnvelopeDefinition](ArrangeEnvelopeDefinition.md).

## Version

Introduced in version January 2025  

