# AsBuiltJointInput.setAsBallJointMotion Method

Parent Object: [AsBuiltJointInput](AsBuiltJointInput.md)  

## Description

Defines the relationship between the two joint geometries as a ball joint.

## Syntax

"asBuiltJointInput_var" is a variable referencing an [AsBuiltJointInput](AsBuiltJointInput.md) object.

```python
# Uses no optional arguments.
returnValue = asBuiltJointInput_var.setAsBallJointMotion(pitchDirection, yawDirection)

# Uses optional arguments.
returnValue = asBuiltJointInput_var.setAsBallJointMotion(pitchDirection, yawDirection, customPitchDirection, customYawDirection)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| pitchDirection | [JointDirections](JointDirections.md) | Defines the direction the pitch angle is measured from. This can be ZAxisJointDirection or CustomJointDirection. If CustomJointDirection is specified then you must also provide a value for the customPitchDirection argument. |
| yawDirection | [JointDirections](JointDirections.md) | Defines the direction the yaw is measured from. This can be XAxisJointDirection or CustomJointDirection. If CustomJointDirection is specified then you must also provide a value for the customYawDirection argument. |
| customPitchDirection | [Base](Base.md) | If the pitchDirection argument is customPitchDirection this argument is used to define the direction the pitch angel is measured from. This can be several types of entities that can define a direction. This is an optional argument whose default value is null. |
| customYawDirection | [Base](Base.md) | If the yawDirection argument is customPitchDirection this argument is used to define the direction the yaw angel is measured from. This can be several types of entities that can define a direction. This is an optional argument whose default value is null. |

## Version

Introduced in version September 2015  

