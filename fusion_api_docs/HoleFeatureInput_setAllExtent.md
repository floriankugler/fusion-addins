# HoleFeatureInput.setAllExtent Method

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Defines the extent of the hole to be through-all. The direction can be either positive, negative.

## Syntax

"holeFeatureInput_var" is a variable referencing a [HoleFeatureInput](HoleFeatureInput.md) object.

```python
returnValue = holeFeatureInput_var.setAllExtent(direction)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| direction | [ExtentDirections](ExtentDirections.md) | The direction of the hole relative to the normal of the sketch plane. |

## Version

Introduced in version August 2014  

