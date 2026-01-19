# HoleFeature.countersinkDiameter Property

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

Returns the model parameter controlling the countersink diameter. This will return null in the case the hole type is not a countersink. The diameter of the countersink can be edited through the returned parameter.

## Syntax

"holeFeature_var" is a variable referencing a HoleFeature object.  

```python
# Get the value of the property.
propertyValue = holeFeature_var.countersinkDiameter
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version August 2014  

