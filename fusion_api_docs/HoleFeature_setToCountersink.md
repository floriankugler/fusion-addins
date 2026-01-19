# HoleFeature.setToCountersink Method

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

Calling this method will change the hole to a countersink hole.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"holeFeature_var" is a variable referencing a [HoleFeature](HoleFeature.md) object.

```python
returnValue = holeFeature_var.setToCountersink(countersinkDiameter, countersinkAngle)
```

## Return Value

| Type    | Description                                       |
|---------|---------------------------------------------------|
| boolean | Returns true if changing the hole was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| countersinkDiameter | [ValueInput](ValueInput.md) | A ValueInput object that defines the countersink diameter. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "3 in"). If no units are specified it is interpreted using the current default units for length. |
| countersinkAngle | [ValueInput](ValueInput.md) | A ValueInput object that defines the countersink angle. If the ValueInput uses a real then it is interpreted as radians. If it is a string then the units can be defined as part of the string (i.e. "120 deg"). If no units are specified it is interpreted using the current default units for length. |

## Version

Introduced in version August 2014  

