# JointGeometry.createByTorusFace Method

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

Creates a new transient JointGeometry object based on a torus BRepFace object.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.JointGeometry.createByTorusFace(face, azimuthAngle, sectionAngle)
```

## Return Value

| Type | Description |
|----|----|
| [JointGeometry](JointGeometry.md) | Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| face | [BRepFace](BRepFace.md) | The torus BRepFace object. |
| azimuthAngle | [JointQuadrantAngleTypes](JointQuadrantAngleTypes.md) | Specifies the azimuth angle relative to the v parameterization of the input face. The zero, or start angle, is where the v parameter of the sphere is zero. This can be determined by using the getPointAtParameter method of the SurfaceEvaluator object obtained from the evaluator property of the BRepFace object. The possible values can be StartJointQuadrantAngleType, QuarterJointQuadrantAngleType, MiddleJointQuadrantAngleType or ThirdQuarterJointQuadrantAngleType. |
| sectionAngle | [JointQuadrantAngleTypes](JointQuadrantAngleTypes.md) | Specifies the angle relative to the start point of the section circle at give azimuth angle. The possible values can be StartJointQuadrantAngleType, QuarterJointQuadrantAngleType, MiddleJointQuadrantAngleType or ThirdQuarterJointQuadrantAngleType. |

## Version

Introduced in version May 2025  

