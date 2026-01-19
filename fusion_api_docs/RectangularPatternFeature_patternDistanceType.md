# RectangularPatternFeature.patternDistanceType Property

Parent Object: [RectangularPatternFeature](RectangularPatternFeature.md)  

## Description

Gets and sets how the distance between elements is computed. Is initialized to ExtentPatternDistanceType when a new RectangularPatternFeatureInput has been created.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"rectangularPatternFeature_var" is a variable referencing a RectangularPatternFeature object.  

```python
# Get the value of the property.
propertyValue = rectangularPatternFeature_var.patternDistanceType

# Set the value of the property.
rectangularPatternFeature_var.patternDistanceType = propertyValue
```

## Property Value

This is a read/write property whose value is a [PatternDistanceType](PatternDistanceType.md).

## Version

Introduced in version November 2014  

