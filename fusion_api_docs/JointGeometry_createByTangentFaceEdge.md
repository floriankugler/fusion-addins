# JointGeometry.createByTangentFaceEdge Method

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

Creates a new transient JointGeometry object based on a BRepFace object as well as a BRepEdge object which is on the BRepFace.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.JointGeometry.createByTangentFaceEdge(face, edge, edgePointType)
```

## Return Value

| Type | Description |
|----|----|
| [JointGeometry](JointGeometry.md) | Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| face | [BRepFace](BRepFace.md) | The cylindrical, conical, spherical, toroidal or spline BRepFace object. |
| edge | [BRepEdge](BRepEdge.md) | A BRepEdge object that is one of the edges on the selected face. |
| edgePointType | [JointTangentFaceEdgePointTypes](JointTangentFaceEdgePointTypes.md) | Specifies the position along the edge where the joint keypoint will be located. The possible values depend on whether the edge is closed or not. For closed edge, the possible values can be StartJointTangentFaceEdgePointType, QuarterJointTangentFaceEdgePointType, MiddleJointTangentFaceEdgePointType or ThirdQuarterJointTangentFaceEdgePointType. For open edge, the possible values can be StartJointTangentFaceEdgePointType, MiddleJointTangentFaceEdgePointType, or EndJointTangentFaceEdgePointType. |

## Version

Introduced in version May 2025  

