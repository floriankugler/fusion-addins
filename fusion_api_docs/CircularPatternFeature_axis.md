# CircularPatternFeature.axis Property

Parent Object: [CircularPatternFeature](CircularPatternFeature.md)  

## Description

Gets and sets the axis of circular pattern. This can be a sketch line, linear edge, construction axis, an edge/sketch curve that defines an axis (circle, etc.) or a face that defines an axis (cylinder, cone, torus, etc.).  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"circularPatternFeature_var" is a variable referencing a CircularPatternFeature object.  

```python
# Get the value of the property.
propertyValue = circularPatternFeature_var.axis

# Set the value of the property.
circularPatternFeature_var.axis = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version November 2014  

