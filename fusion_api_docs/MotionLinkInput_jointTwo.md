# MotionLinkInput.jointTwo Property

Parent Object: [MotionLinkInput](MotionLinkInput.md)  

## Description

Gets and sets the second Joint or AsBuiltJoint for this MotionLink. This can be a joint or null, when this is set to null then the two motions are from the same joint specified by jointOne. A joint whose joint motion is a RigidJointMotion type is never valid as the second joint.

## Syntax

"motionLinkInput_var" is a variable referencing a MotionLinkInput object.  

```python
# Get the value of the property.
propertyValue = motionLinkInput_var.jointTwo

# Set the value of the property.
motionLinkInput_var.jointTwo = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version November 2025  

