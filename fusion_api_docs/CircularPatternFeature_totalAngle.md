# CircularPatternFeature.totalAngle Property

Parent Object: [CircularPatternFeature](CircularPatternFeature.md)  

## Description

Returns the parameter controlling the total angle. To edit the angle use properties on the parameter to edit its value. This property returns null in the case where the feature is non-parametric. A negative value can be used to change the direction of the pattern.

## Syntax

"circularPatternFeature_var" is a variable referencing a CircularPatternFeature object.  

```python
# Get the value of the property.
propertyValue = circularPatternFeature_var.totalAngle
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version November 2014  

