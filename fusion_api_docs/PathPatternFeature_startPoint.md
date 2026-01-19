# PathPatternFeature.startPoint Property

Parent Object: [PathPatternFeature](PathPatternFeature.md)  

## Description

Gets and sets the start point on the path to count the distance. It's between 0 and 1. 0 means start point of the path, 1 means end point of the path.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"pathPatternFeature_var" is a variable referencing a PathPatternFeature object.  

```python
# Get the value of the property.
propertyValue = pathPatternFeature_var.startPoint

# Set the value of the property.
pathPatternFeature_var.startPoint = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version November 2014  

