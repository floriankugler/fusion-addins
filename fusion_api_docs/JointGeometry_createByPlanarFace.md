# JointGeometry.createByPlanarFace Method

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

Creates a new transient JointGeometry object based on a planar BRepFace object. A JointGeometry object can be used to create a joint or joint origin.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.JointGeometry.createByPlanarFace(face, edge, keyPointType)
```

## Return Value

| Type | Description |
|----|----|
| [JointGeometry](JointGeometry.md) | Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| face | [BRepFace](BRepFace.md) | The planar BRepFace object |
| edge | [BRepEdge](BRepEdge.md) | A BRepEdge edge object that is one of the edges of the specified face. This argument can be null in the case where the keyPointType is CenterKeypoint indicating the center of the face is to be used. When an edge is used, the keyPointType specifies the position along the edge for the keypoint. |
| keyPointType | [JointKeyPointTypes](JointKeyPointTypes.md) | Specifies the position along the edge where the joint keypoint will be located. For open edges this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint. For closed edges (i.e. circles), it must be CenterKeyPoint. When no edge is specified, it must be CenterKeyPoint indicating the center of area of the face is to be used. |

## Samples

| Name | Description |
|----|----|
| [Joint Origin Sample](JointOriginSample_Sample.md) | Demonstrates creating a new Joint Origin. |
| [Joint API Sample](JointSample_Sample.md) | Demonstrates creating a new joint. |

## Version

Introduced in version July 2015  

