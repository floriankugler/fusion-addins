# JointGeometry.createBySplineFace Method

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

Creates a new transient JointGeometry object based on a spline BRepFace object.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.JointGeometry.createBySplineFace(face, paramU, paramV)
```

## Return Value

| Type | Description |
|----|----|
| [JointGeometry](JointGeometry.md) | Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| face | [BRepFace](BRepFace.md) | The spline BRepFace object. |
| paramU | [JointKeyPointTypes](JointKeyPointTypes.md) | Specifies the u parameter of the input spline face where the joint keypoint will be located. The possible values can be StartKeyPoint, MiddleKeyPoint or EndKeyPoint. |
| paramV | [JointKeyPointTypes](JointKeyPointTypes.md) | Specifies the v parameter of the input spline face where the joint keypoint will be located. The possible values can be StartKeyPoint, MiddleKeyPoint or EndKeyPoint. |

## Version

Introduced in version May 2025  

