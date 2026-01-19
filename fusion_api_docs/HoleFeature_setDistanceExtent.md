# HoleFeature.setDistanceExtent Method

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

Defines the depth of the hole using a specific distance.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"holeFeature_var" is a variable referencing a [HoleFeature](HoleFeature.md) object.

```python
returnValue = holeFeature_var.setDistanceExtent(distance)
```

## Return Value

| Type    | Description                                        |
|---------|----------------------------------------------------|
| boolean | Returns true if setting the extent was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| distance | [ValueInput](ValueInput.md) | The depth of the hole. If a real is specified the value is in centimeters. If a string is specified the units are derived from the string. If no units are specified, the default units of the document are used. |

## Version

Introduced in version August 2014  

