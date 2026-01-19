# AsBuiltJointInput.setAsSliderJointMotion Method

Parent Object: [AsBuiltJointInput](AsBuiltJointInput.md)  

## Description

Defines the relationship between the two joint geometries as a slider joint.

## Syntax

"asBuiltJointInput_var" is a variable referencing an [AsBuiltJointInput](AsBuiltJointInput.md) object.

```python
# Uses no optional arguments.
returnValue = asBuiltJointInput_var.setAsSliderJointMotion(sliderDirection)

# Uses optional arguments.
returnValue = asBuiltJointInput_var.setAsSliderJointMotion(sliderDirection, customSliderDirectionEntity)
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

## Version

Introduced in version September 2015  

