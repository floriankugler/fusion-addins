# ArrangeFeature.unusedComponents Property

Parent Object: [ArrangeFeature](ArrangeFeature.md)  

## Description

Returns an array of ArrangeComponent objects that did not fit in the arrangement. This is most useful in the case where partial arrange has been enabled, which means some components may have been arranged and others were left out.  

To use this property, you need to position the timeline marker immediately before the Arrange feature. This can be accomplished using the following code: arrangeFeature.timelineObject.rollTo(True)

## Syntax

"arrangeFeature_var" is a variable referencing an ArrangeFeature object.  

```python
# Get the value of the property.
propertyValue = arrangeFeature_var.unusedComponents
```

## Property Value

This is a read only property whose value is an array of type [ArrangeComponent](ArrangeComponent.md).

## Version

Introduced in version January 2025  

