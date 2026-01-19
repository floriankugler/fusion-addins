# BallJointMotion.customYawDirectionEntity Property

Parent Object: [BallJointMotion](BallJointMotion.md)  

## Description

This property defines a custom yaw direction and can be set using various types of entities that can infer a direction. For example, a linear edge, sketch line, planar face, and cylindrical face.This property is only valid in the case where the yawDirection property returns CustomJointDirection. Setting this property will automatically set the yawDirection property to CustomJointDirection.  

To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True)

## Syntax

"ballJointMotion_var" is a variable referencing a BallJointMotion object.  

```python
# Get the value of the property.
propertyValue = ballJointMotion_var.customYawDirectionEntity

# Set the value of the property.
ballJointMotion_var.customYawDirectionEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version July 2015  

