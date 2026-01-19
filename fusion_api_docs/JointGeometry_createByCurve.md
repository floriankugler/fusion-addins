# JointGeometry.createByCurve Method

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

Creates a new transient JointGeometry object using a BRepEdge or SketchCurve as input. A JointGeometry object can be used to create a joint or joint origin.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.JointGeometry.createByCurve(curve, keyPointType)
```

## Return Value

| Type | Description |
|----|----|
| [JointGeometry](JointGeometry.md) | Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| curve | [Base](Base.md) | Input BRepEdge or SketchCurve. |
| keyPointType | [JointKeyPointTypes](JointKeyPointTypes.md) | The position on the curve where to position the joint coordinate system. For any open curves the valid types are StartKeyPoint, MiddleKeyPoint, CenterKeyPoint and EndKeyPoint. For circular and elliptical shaped curves the option is CenterKeyPoint. For closed spline curves either StartKeyPoint or EndKeyPoint can be used and the result is the same. |

## Samples

| Name | Description |
|----|----|
| [BallJointMotion API Sample](BallJointMotionSample_Sample.md) | Demonstrates creating a joint with ball joint motion |
| [CylindricalJointMotion API Sample](CylindricalJointMotionSample_Sample.md) | Demonstrates creating a joint with cylindrical joint motion. |
| [Joint API Sample](JointSample_Sample.md) | Demonstrates creating a new joint. |
| [Pin Slot Joint Motion API Sample](PinSlotJointMotionSample_Sample.md) | Demonstrates creating a joint with pin slot joint motion |
| [Planar Joint Motion API Sample](PlanarJointMotionSample_Sample.md) | Demonstrates creating a joint with planar joint motion |
| [SliderJointMotion API Sample](SliderJointMotionSample_Sample.md) | Demonstrates creating a joint with slider joint motion. |

## Version

Introduced in version July 2015  

