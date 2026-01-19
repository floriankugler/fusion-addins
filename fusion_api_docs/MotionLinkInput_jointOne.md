# MotionLinkInput.jointOne Property

Parent Object: [MotionLinkInput](MotionLinkInput.md)  

## Description

Gets and sets the first Joint or AsBuiltJoint for this MotionLink. When you link two motions from the same joint, a valid joint should have its joint motion type of BallJointType, CylindricalJointType, PinSlotJointType or PlanarJointType. A joint whose joint motion is a RigidJointMotion type is never valid as the first joint..

## Syntax

"motionLinkInput_var" is a variable referencing a MotionLinkInput object.  

```python
# Get the value of the property.
propertyValue = motionLinkInput_var.jointOne

# Set the value of the property.
motionLinkInput_var.jointOne = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version November 2025  

