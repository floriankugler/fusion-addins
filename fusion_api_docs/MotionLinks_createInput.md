# MotionLinks.createInput Method

Parent Object: [MotionLinks](MotionLinks.md)  

## Description

Creates a MotionLinkInput object, which is the API equivalent to the Motion Link command dialog. You can use methods and properties on the returned object to set the desired options, similar to providing input and setting options in the MotionLink command dialog. Once the settings are defined you call the MotionLinks.add method passing in the MotionLinkInput object to create the actual MotionLink.

## Syntax

"motionLinks_var" is a variable referencing a [MotionLinks](MotionLinks.md) object.

```python
# Uses no optional arguments.
returnValue = motionLinks_var.createInput(jointOne)

# Uses optional arguments.
returnValue = motionLinks_var.createInput(jointOne, jointTwo)
```

## Return Value

| Type | Description |
|----|----|
| [MotionLinkInput](MotionLinkInput.md) | Returns the MotionLinkInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| jointOne | [Base](Base.md) | Inputs the first Joint or AsBuiltJoint to link its motion(s). If the jointTwo is set to null, then two motions from the jointOne will be linked, and in this case a valid Joint or AsBuiltJoint for jointOne should have its joint motion type of BallJointType, CylindricalJointType, PinSlotJointType or PlanarJointType. A Joint or AsBuiltJoint whose joint motion is a RigidJointMotion type is never valid as the first joint. |
| jointTwo | [Base](Base.md) | Inputs the second Joint or AsBuiltJoint to link its motion. If this is set to null, then the two motions from the jointOne will be linked. A Joint or AsBuiltJoint whose joint motion is a RigidJointMotion type is never valid as the second joint. This is an optional argument whose default value is null. |

## Version

Introduced in version November 2025  

