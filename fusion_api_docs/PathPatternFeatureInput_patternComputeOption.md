# PathPatternFeatureInput.patternComputeOption Property

Parent Object: [PathPatternFeatureInput](PathPatternFeatureInput.md)  

## Description

Gets and sets the compute option when patterning features. The default value for this is AdjustPatternCompute. This property only applies when patterning features and is ignored in the direct modeling environment.

## Syntax

"pathPatternFeatureInput_var" is a variable referencing a PathPatternFeatureInput object.  

```python
# Get the value of the property.
propertyValue = pathPatternFeatureInput_var.patternComputeOption

# Set the value of the property.
pathPatternFeatureInput_var.patternComputeOption = propertyValue
```

## Property Value

This is a read/write property whose value is a [PatternComputeOptions](PatternComputeOptions.md).

## Version

Introduced in version November 2015  

