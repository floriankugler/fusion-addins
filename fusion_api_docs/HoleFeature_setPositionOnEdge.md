# HoleFeature.setPositionOnEdge Method

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

Redefines the position and orientation of the hole to be on the start, end or center of an edge.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"holeFeature_var" is a variable referencing a [HoleFeature](HoleFeature.md) object.

```python
returnValue = holeFeature_var.setPositionOnEdge(planarEntity, edge, position)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntity | [Base](Base.md) | The planar BRepFace or ConstructionPlane object that defines the orientation of the hole and start of the hole. The natural direction of the hole will be opposite the normal of the face or construction plane. |
| edge | [BRepEdge](BRepEdge.md) | The edge to position the hole on. |
| position | [HoleEdgePositions](HoleEdgePositions.md) | The position along the edge to place the hole. |

## Version

Introduced in version August 2014  

