# RectangularPatternFeature.directionOneEntity Property

Parent Object: [RectangularPatternFeature](RectangularPatternFeature.md)  

## Description

Gets and sets the first direction entity. This can be a linear edge, construction axis, sketch line or rectangular pattern feature. If a rectangular pattern feature is set, the directionOneEntity and directionTwoEntity properties return the same rectangular pattern feature.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"rectangularPatternFeature_var" is a variable referencing a RectangularPatternFeature object.  

```python
# Get the value of the property.
propertyValue = rectangularPatternFeature_var.directionOneEntity

# Set the value of the property.
rectangularPatternFeature_var.directionOneEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version November 2014  

