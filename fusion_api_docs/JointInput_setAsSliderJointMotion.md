# JointInput.setAsSliderJointMotion Method

Parent Object: [JointInput](JointInput.md)  

## Description

Defines the relationship between the two joint geometries as a slider joint.

## Syntax

"jointInput_var" is a variable referencing a [JointInput](JointInput.md) object.

```python
# Uses no optional arguments.
returnValue = jointInput_var.setAsSliderJointMotion(sliderDirection)

# Uses optional arguments.
returnValue = jointInput_var.setAsSliderJointMotion(sliderDirection, customSliderDirectionEntity)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| sliderDirection | [JointDirections](JointDirections.md) | Specifies which axis the slide direction is along. If this is set to CustomJointDirection then the customSliderDirectionEntity argument must also be provided. |
| customSliderDirectionEntity | [Base](Base.md) | If the sliderDirection is CustomJointDirection this argument is used to specify the entity that defines the custom slider direction. This can be several types of entities that can define a direction. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [BallJointMotion API Sample](BallJointMotionSample_Sample.md) | Demonstrates creating a joint with ball joint motion |
| [Pin Slot Joint Motion API Sample](PinSlotJointMotionSample_Sample.md) | Demonstrates creating a joint with pin slot joint motion |
| [Planar Joint Motion API Sample](PlanarJointMotionSample_Sample.md) | Demonstrates creating a joint with planar joint motion |
| [SliderJointMotion API Sample](SliderJointMotionSample_Sample.md) | Demonstrates creating a joint with slider joint motion. |

## Version

Introduced in version July 2015  

