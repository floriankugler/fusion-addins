# PathPatternFeature.patternComputeOption Property

Parent Object: [PathPatternFeature](PathPatternFeature.md)  

## Description

Gets and sets the compute option for this pattern feature. This property only applies when patterning features and is ignored in the direct modeling environment.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"pathPatternFeature_var" is a variable referencing a PathPatternFeature object.  

```python
# Get the value of the property.
propertyValue = pathPatternFeature_var.patternComputeOption

# Set the value of the property.
pathPatternFeature_var.patternComputeOption = propertyValue
```

## Property Value

This is a read/write property whose value is a [PatternComputeOptions](PatternComputeOptions.md).

## Version

Introduced in version November 2015  

