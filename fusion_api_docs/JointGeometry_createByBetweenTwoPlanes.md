# JointGeometry.createByBetweenTwoPlanes Method

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

Creates a new transient JointGeometry object based on a plane bisecting the two input planes.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.JointGeometry.createByBetweenTwoPlanes(planeOne, planeTwo, entityOne, entityTwo, keyPointType)
```

## Return Value

| Type | Description |
|----|----|
| [JointGeometry](JointGeometry.md) | Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| planeOne | [Base](Base.md) | The first planar entity that the joint origin will be created between. This can be a planar BRepFace or a ConstructionPlane object. |
| planeTwo | [Base](Base.md) | The second planar entity that the joint origin will be created between. This can be a planar BRepFace or a ConstructionPlane object. |
| entityOne | [Base](Base.md) | Specifies the entity that is used to define the keypoint. This can be many types of geometry including edges, planar and non-planar faces, profiles, and sketch geometry. |
| entityTwo | [Base](Base.md) | If the entityOne argument is a planar BRepFace or a Profile, then this argument specifies either an edge on the face or a sketch curve on the profile. For a planar face this argument is optional in the case where the keyPointType argument is CenterKeyPoint indicating the center of area of the face is to be used. |
| keyPointType | [JointKeyPointTypes](JointKeyPointTypes.md) | Specifies the position on the keyPointGeometry where the keypoint will be defined. This keypoint is then projected onto the plane to define the position of the joint geometry. The values that are valid for this argument depend on the type of geometry specified for the geometry and edgeOrCurve arguments. If the geometry argument is a planar face and the edgeOrCurve argument is an open BRepEdge object then this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint. If the geometry argument is a planar face and the edgeOrCurve argument is a closed BRepEdge object (i.e. circles), it must be CenterKeyPoint. If the geometry argument is a planar face and the edgeOrCurve argument is null, then this must be CenterKeyPoint indicating the center of area of the face. If the geometry argument is a non-planar face (cylinder, cone, sphere, or torus) this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint for cylinders and cones but must be CenterKeyPoint for spheres and tori. The edgeOrCurve argument is ignored in this case. If the geometry argument is a profile and the edgeOrCurve argument is null this can be CenterKeyPoint indicating the center of area of the profile. If the geometry argument is a profile and the edgeOrCurve argument is an open sketch curve on the profile then this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint. If the geometry argument is a profile and the edgeOrCurve argument is a closed sketch curve (i.e. circles), it must be CenterKeyPoint. |

## Samples

| Name | Description |
|----|----|
| [Joint Origin Between Two Faces Sample](JointOrigin2Planes_Sample.md) | Demonstrates creating a new Joint Origin between two planes. |

## Version

Introduced in version January 2016  

