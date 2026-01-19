# CircularPatternFeature.quantity Property

Parent Object: [CircularPatternFeature](CircularPatternFeature.md)  

## Description

Returns the parameter controlling the number of pattern elements, including any suppressed elements. To edit the quantity use properties on the parameter to edit its value. This property returns null in the case where the feature is non-parametric.

## Syntax

"circularPatternFeature_var" is a variable referencing a CircularPatternFeature object.  

```python
# Get the value of the property.
propertyValue = circularPatternFeature_var.quantity
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version November 2014  

