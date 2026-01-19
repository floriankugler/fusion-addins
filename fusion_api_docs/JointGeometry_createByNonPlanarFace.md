# JointGeometry.createByNonPlanarFace Method

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

Creates a new transient JointGeometry object based on a non-planar analytical BRepFace object. This is limited to cylinders, cones, spheres, and tori. A JointGeometry object can be used to create a joint or joint origin.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.JointGeometry.createByNonPlanarFace(face, keyPointType)
```

## Return Value

| Type | Description |
|----|----|
| [JointGeometry](JointGeometry.md) | Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| face | [BRepFace](BRepFace.md) | The cylindrical, conical, spherical, or toroidal BRepFace object. |
| keyPointType | [JointKeyPointTypes](JointKeyPointTypes.md) | Specifies the position relative to the input face where the joint keypoint will be located. For cylinders and cones this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint. For spheres and tori this must be CenterKeyPoint. |

## Samples

| Name | Description |
|----|----|
| [RevoluteJointMotion API Sample](RevoluteJointMotionSample_Sample.md) | Demonstrates creating a joint with revolute joint motion. |

## Version

Introduced in version July 2015  

