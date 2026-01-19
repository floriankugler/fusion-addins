# PathPatternFeature.isFlipDirection Property

Parent Object: [PathPatternFeature](PathPatternFeature.md)  

## Description

Gets and sets if flip the direction from start point.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"pathPatternFeature_var" is a variable referencing a PathPatternFeature object.  

```python
# Get the value of the property.
propertyValue = pathPatternFeature_var.isFlipDirection

# Set the value of the property.
pathPatternFeature_var.isFlipDirection = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2014  

