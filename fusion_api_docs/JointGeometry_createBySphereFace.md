# JointGeometry.createBySphereFace Method

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

Creates a new transient JointGeometry object based on a sphere BRepFace object.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.JointGeometry.createBySphereFace(face, azimuthAngle, polarAngle)
```

## Return Value

| Type | Description |
|----|----|
| [JointGeometry](JointGeometry.md) | Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| face | [BRepFace](BRepFace.md) | The sphere BRepFace object. |
| azimuthAngle | [JointQuadrantAngleTypes](JointQuadrantAngleTypes.md) | Specifies the azimuth angle relative to the v parameterization of the input face. The zero, or start angle, is where the v parameter of the sphere is zero. This can be determined by using the getPointAtParameter method of the SurfaceEvaluator object obtained from the evaluator property of the BRepFace object. The possible values can be StartJointQuadrantAngleType, QuarterJointQuadrantAngleType, MiddleJointQuadrantAngleType or ThirdQuarterJointQuadrantAngleType. |
| polarAngle | [JointKeyPointTypes](JointKeyPointTypes.md) | Specifies the polar angle relative to the u parameterization of the input face. The zero, or start angle, is where the u parameter of the sphere is zero. This can be determined by using the getPointAtParameter method of the SurfaceEvaluator object obtained from the evaluator property of the BRepFace object. The possible values can be StartKeyPoint for the north pole, MiddleKeyPoint for points on the equator, or EndKeyPoint for the south pole. |

## Version

Introduced in version May 2025  

