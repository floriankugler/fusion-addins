# PatchFeature.getContinuity Method

Parent Object: [PatchFeature](PatchFeature.md)  

## Description

Gets the continuity used for each edge in the boundary.  

To call this method, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"patchFeature_var" is a variable referencing a [PatchFeature](PatchFeature.md) object.  

```python
(returnValue, edges, continuity, weight, isContinuityDirectionFlipped) = patchFeature_var.getContinuity()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| edges | BRepEdge[] | Output array containing all of the BRepEdge objects in the boundary. |
| continuity | integer[] | Output array the same size as the edges array that defines the continuity to apply to the edge in the same index in the edges array. The values are obtained from the SurfaceContinuityTypes enum and passed in as an integers. |
| weight | double[] | Output array the same size as the edges array that defines the weight applied to the edge in the same index in the edges array. If the continuity of an edge is ConnectedSurfaceContinuityType, the weight value should be ignored. |
| isContinuityDirectionFlipped | boolean[] | Output array the same size as the edges array that defines which of the two faces the edge connects to is used in computing the continuity direction. If the continuity is ConnectedSurfaceContinuityType or the edge is an open edge and only connected to a single face, the value should be ignored. If false, the face associated with the first co-edge returned by the edge is used. |

## Version

Introduced in version November 2022  

