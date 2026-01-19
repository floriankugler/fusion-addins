# SilhouetteSplitFeature.targetBody Property

Parent Object: [SilhouetteSplitFeature](SilhouetteSplitFeature.md)  

## Description

Gets and sets the solid body to split.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"silhouetteSplitFeature_var" is a variable referencing a SilhouetteSplitFeature object.  

```python
# Get the value of the property.
propertyValue = silhouetteSplitFeature_var.targetBody

# Set the value of the property.
silhouetteSplitFeature_var.targetBody = propertyValue
```

## Property Value

This is a read/write property whose value is a [BRepBody](BRepBody.md).

## Version

Introduced in version June 2015  

