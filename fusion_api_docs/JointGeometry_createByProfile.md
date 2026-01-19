# JointGeometry.createByProfile Method

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

Creates a new transient JointGeometry object based on a planar BRepFace object. A JointGeometry object can be used to create a joint or joint origin.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.JointGeometry.createByProfile(profile, sketchCurve, keyPointType)
```

## Return Value

| Type | Description |
|----|----|
| [JointGeometry](JointGeometry.md) | Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| profile | [Profile](Profile.md) | The Profile object. |
| sketchCurve | [SketchCurve](SketchCurve.md) | A sketch curve that is part of the input profile. This argument can be null in the case where the keyPointType is CenterKeypoint indicating the center of the profile is to be used. When a curve is used, the keyPointType specifies the position along the curve for the keypoint. |
| keyPointType | [JointKeyPointTypes](JointKeyPointTypes.md) | Specifies the position along the curve where the joint keypoint will be located. For open curves (lines, arcs, elliptical arcs, and open splines) this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint. For closed analytic (circles and ellipses), it must be CenterKeyPoint. When no curve is specified, it must be CenterKeyPoint indicating the center of area of the profile is to be used. |

## Samples

| Name | Description |
|----|----|
| [RevoluteJointMotion API Sample](RevoluteJointMotionSample_Sample.md) | Demonstrates creating a joint with revolute joint motion. |

## Version

Introduced in version July 2015  

