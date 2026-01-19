# HoleFeature.holeDiameter Property

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

Returns the model parameter controlling the hole diameter. The diameter of the hole can be edited through the returned parameter object.  

If there is a thread associated with the hole the thread definition controls the diameter of the hole. Even though there is a parameter for the diameter, its value is ignored when there is a thread.

## Syntax

"holeFeature_var" is a variable referencing a HoleFeature object.  

```python
# Get the value of the property.
propertyValue = holeFeature_var.holeDiameter
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version August 2014  

