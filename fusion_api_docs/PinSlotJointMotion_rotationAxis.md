# PinSlotJointMotion.rotationAxis Property

Parent Object: [PinSlotJointMotion](PinSlotJointMotion.md)  

## Description

Gets and sets the direction of the axis of rotation. This can be set to XAxisJointDirection, YAxisJointDirection, or ZAxisJointDirection. It can return those three directions and CustomJointDirection. If this returns CustomJointDirection then the customRotationAxisEntity will return an entity that defines the axis. If there is a custom rotation axis defined and this property is set to one of the three standard axes, the custom rotation will be removed and customRotationAxisEntity will return null.

## Syntax

"pinSlotJointMotion_var" is a variable referencing a PinSlotJointMotion object.  

```python
# Get the value of the property.
propertyValue = pinSlotJointMotion_var.rotationAxis

# Set the value of the property.
pinSlotJointMotion_var.rotationAxis = propertyValue
```

## Property Value

This is a read/write property whose value is a [JointDirections](JointDirections.md).

## Version

Introduced in version July 2015  

