# SplitBodyFeature.splitBodies Property

Parent Object: [SplitBodyFeature](SplitBodyFeature.md)  

## Description

Gets and sets the input solid or open bodies that are split.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"splitBodyFeature_var" is a variable referencing a SplitBodyFeature object.  

```python
# Get the value of the property.
propertyValue = splitBodyFeature_var.splitBodies

# Set the value of the property.
splitBodyFeature_var.splitBodies = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version June 2015  

