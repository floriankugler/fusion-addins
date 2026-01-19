# AsBuiltJoint.setAsSliderJointMotion Method

Parent Object: [AsBuiltJoint](AsBuiltJoint.md)  

## Description

Redefines the relationship between the two joint geometries as a slider joint.  

To use this method, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True)

## Syntax

"asBuiltJoint_var" is a variable referencing an [AsBuiltJoint](AsBuiltJoint.md) object.

```python
# Uses no optional arguments.
returnValue = asBuiltJoint_var.setAsSliderJointMotion(sliderDirection)

# Uses optional arguments.
returnValue = asBuiltJoint_var.setAsSliderJointMotion(sliderDirection, geometry, customSliderDirectionEntity)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| sliderDirection | [JointDirections](JointDirections.md) | Specifies which axis the slide direction is along. If this is set to CustomJointDirection then the customSliderDirectionEntity argument must also be provided. |
| geometry | [JointGeometry](JointGeometry.md) | Redefines the joint geometry. If not provided, the existing geometry is used. This argument is required if the current joint motion is rigid. This is an optional argument whose default value is null. |
| customSliderDirectionEntity | [Base](Base.md) | If the sliderDirection is CustomJointDirection this argument is used to specify the entity that defines the custom slider direction. This can be several types of entities that can define a direction. This is an optional argument whose default value is null. |

## Version

Introduced in version September 2015  

