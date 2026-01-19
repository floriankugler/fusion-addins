# DraftFeature.isTangentChain Property

Parent Object: [DraftFeature](DraftFeature.md)  

## Description

Gets and sets if any faces that are tangentially connected to any of the input faces will also be drafted. It defaults to true.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"draftFeature_var" is a variable referencing a DraftFeature object.  

```python
# Get the value of the property.
propertyValue = draftFeature_var.isTangentChain

# Set the value of the property.
draftFeature_var.isTangentChain = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2015  

