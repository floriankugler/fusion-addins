# BallJointMotion.pitchDirection Property

Parent Object: [BallJointMotion](BallJointMotion.md)  

## Description

Gets and sets the direction that the pitch is measured from. This can only be set to ZAxisJointDirection and can return ZAxisJointDirection or CustomJointDirection. If this returns CustomJointDirection then the customNormalDirectionEntity will return an entity that defines the direction. If there is a custom direction defined and this property is set to ZAxisJointDirection, the custom direction will be removed and customNormalDirectionEntity will return null.

## Syntax

"ballJointMotion_var" is a variable referencing a BallJointMotion object.  

```python
# Get the value of the property.
propertyValue = ballJointMotion_var.pitchDirection

# Set the value of the property.
ballJointMotion_var.pitchDirection = propertyValue
```

## Property Value

This is a read/write property whose value is a [JointDirections](JointDirections.md).

## Version

Introduced in version July 2015  

