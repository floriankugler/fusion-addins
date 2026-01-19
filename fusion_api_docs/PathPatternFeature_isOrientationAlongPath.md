# PathPatternFeature.isOrientationAlongPath Property

Parent Object: [PathPatternFeature](PathPatternFeature.md)  

## Description

Gets and sets if the orientation is along path. If false, the orientation is identical.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"pathPatternFeature_var" is a variable referencing a PathPatternFeature object.  

```python
# Get the value of the property.
propertyValue = pathPatternFeature_var.isOrientationAlongPath

# Set the value of the property.
pathPatternFeature_var.isOrientationAlongPath = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2014  

