# CircularPatternFeature.patternComputeOption Property

Parent Object: [CircularPatternFeature](CircularPatternFeature.md)  

## Description

Gets and sets the compute option for this pattern feature. This property only applies when patterning features and is ignored in the direct modeling environment.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"circularPatternFeature_var" is a variable referencing a CircularPatternFeature object.  

```python
# Get the value of the property.
propertyValue = circularPatternFeature_var.patternComputeOption

# Set the value of the property.
circularPatternFeature_var.patternComputeOption = propertyValue
```

## Property Value

This is a read/write property whose value is a [PatternComputeOptions](PatternComputeOptions.md).

## Version

Introduced in version November 2015  

