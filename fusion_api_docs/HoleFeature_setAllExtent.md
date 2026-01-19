# HoleFeature.setAllExtent Method

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

Defines the extent of the hole to be through-all. The direction can be either positive, negative.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"holeFeature_var" is a variable referencing a [HoleFeature](HoleFeature.md) object.

```python
returnValue = holeFeature_var.setAllExtent(direction)
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

