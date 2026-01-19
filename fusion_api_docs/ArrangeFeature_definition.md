# ArrangeFeature.definition Property

Parent Object: [ArrangeFeature](ArrangeFeature.md)  

## Description

Returns a definition object that provides access to the information defining this arrange feature and provides access to the resulting arrangement of occurrences.  

To use this property, you need to position the timeline marker immediately before the Arrange feature. This can be accomplished using the following code: arrangeFeature.timelineObject.rollTo(True)

## Syntax

"arrangeFeature_var" is a variable referencing an ArrangeFeature object.  

```python
# Get the value of the property.
propertyValue = arrangeFeature_var.definition
```

## Property Value

This is a read only property whose value is an [ArrangeDefinition](ArrangeDefinition.md).

## Version

Introduced in version January 2025  

