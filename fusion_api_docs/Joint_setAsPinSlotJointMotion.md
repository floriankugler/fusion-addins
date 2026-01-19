# Joint.setAsPinSlotJointMotion Method

Parent Object: [Joint](Joint.md)  

## Description

Redefines the relationship between the two joint geometries as a pin-slot joint.  

This method will fail in the case where the jointType property returns InferredJointType.  

To use this method, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True)

## Syntax

"joint_var" is a variable referencing a [Joint](Joint.md) object.

```python
# Uses no optional arguments.
returnValue = joint_var.setAsPinSlotJointMotion(rotationAxis, slideDirection)

# Uses optional arguments.
returnValue = joint_var.setAsPinSlotJointMotion(rotationAxis, slideDirection, customRotationAxisEntity, customSlideDirectionEntity)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| rotationAxis | [JointDirections](JointDirections.md) | Specifies which axis the rotation is around. If this is set to CustomJointDirection then the customRotationAxisEntity argument must also be provided. |
| slideDirection | [JointDirections](JointDirections.md) | Specifies which axis the slide direction is along. If this is set to CustomJointDirection then the customSlideDirectionEntity argument must also be provided. |
| customRotationAxisEntity | [Base](Base.md) | If the rotationAxis is customAxisEntity this argument is used to specify the entity that defines the custom axis of rotation. This can be several types of entities that an axis can be derived This is an optional argument whose default value is null. |
| customSlideDirectionEntity | [Base](Base.md) | If the slideDirection is CustomJointDirection this argument is used to specify the entity that defines the custom slide direction. This can be several types of entities that can define a direction. This is an optional argument whose default value is null. |

## Version

Introduced in version July 2015  

