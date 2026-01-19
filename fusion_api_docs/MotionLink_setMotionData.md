# MotionLink.setMotionData Method

Parent Object: [MotionLink](MotionLink.md)  

## Description

Method that sets the motion data.

## Syntax

"motionLink_var" is a variable referencing a [MotionLink](MotionLink.md) object.

```python
# Uses no optional arguments.
returnValue = motionLink_var.setMotionData(motionOne, valueOne, motionTwo, valueTwo)

# Uses optional arguments.
returnValue = motionLink_var.setMotionData(motionOne, valueOne, motionTwo, valueTwo, isReversed)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| motionOne | [JointMotionTypes](JointMotionTypes.md) | Specifies the first motion to link. |
| valueOne | [ValueInput](ValueInput.md) | Specifies the first motion link value. If the ValueInput uses a real then it is interpreted as centimeters for length and radians for angle. If it is a string then the units can be defined as part of the string (i.e. "2 in" or "60 deg") or if no units are specified it is interpreted using the current default units for length or angle. |
| motionTwo | [JointMotionTypes](JointMotionTypes.md) | Specifies the second motion to link. |
| valueTwo | [ValueInput](ValueInput.md) | Specifies the second motion link value. If the ValueInput uses a real then it is interpreted as centimeters for length and radians for angle. If it is a string then the units can be defined as part of the string (i.e. "2 in" or "60 deg") or if no units are specified it is interpreted using the current default units for length or angle. |
| isReversed | boolean | Optional argument that specifies whether to reverse the direction of the motion. This is an optional argument whose default value is False. |

## Version

Introduced in version November 2025  

