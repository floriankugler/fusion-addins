# DraftFeature.isDirectionFlipped Property

Parent Object: [DraftFeature](DraftFeature.md)  

## Description

Gets and sets if the direction of the draft is flipped.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"draftFeature_var" is a variable referencing a DraftFeature object.  

```python
# Get the value of the property.
propertyValue = draftFeature_var.isDirectionFlipped

# Set the value of the property.
draftFeature_var.isDirectionFlipped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2015  

