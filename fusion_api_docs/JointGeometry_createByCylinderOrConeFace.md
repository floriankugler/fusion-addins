# JointGeometry.createByCylinderOrConeFace Method

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

Creates a new transient JointGeometry object based on a cylinder or cone BRepFace object.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.JointGeometry.createByCylinderOrConeFace(face, angle, height)
```

## Return Value

| Type | Description |
|----|----|
| [JointGeometry](JointGeometry.md) | Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| face | [BRepFace](BRepFace.md) | The cylindrical or conical BRepFace object. |
| angle | [JointQuadrantAngleTypes](JointQuadrantAngleTypes.md) | Specifies the angle relative to the parameterization of the input face. The zero, or start angle, is where the v parameter of the cylinder is zero. This can be determined by using the getPointAtParameter method of the SurfaceEvaluator object obtained from the evaluator property of the BRepFace object. The possible values can be StartJointQuadrantAngleType, QuarterJointQuadrantAngleType, MiddleJointQuadrantAngleType or ThirdQuarterJointQuadrantAngleType. |
| height | [JointKeyPointTypes](JointKeyPointTypes.md) | Specifies the vertical position relative to the bottom of the cylinder at the given angle. The possible values can be StartKeyPoint, MiddleKeyPoint or EndKeyPoint. |

## Version

Introduced in version May 2025  

