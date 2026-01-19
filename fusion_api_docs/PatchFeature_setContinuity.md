# PatchFeature.setContinuity Method

Parent Object: [PatchFeature](PatchFeature.md)  

## Description

Sets the continuity to use for each edge in the boundary. The arrays for the arguments correspond to B-Rep edges in the boundary. You can use the getContinuity method to get the list of edges to know their order. This order applies to the arrays provided for the arguments.

## Syntax

"patchFeature_var" is a variable referencing a [PatchFeature](PatchFeature.md) object.

```python
returnValue = patchFeature_var.setContinuity(continuity, weight, isContinuityDirectionFlipped)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| continuity | integer[] | An array whose size of the number of B-Rep edges in the boundary. You can use the getContinuity method to get the list of edges, so you know the number and order of the edges. The continuity array defines the type of continuity to apply to the edge at the same index. The values are obtained from the SurfaceContinuityTypes enum and passed in as an integer. |
| weight | double[] | An array whose size is the number of B-Rep edges in the boundary. You can use the getContinuity method to get the list of edges, so you know the number and order of the edges. The weight array defines the weight to apply to the edge at the same index. If the continuity of an edge is ConnectedSurfaceContinuityType, the weight value is ignored. |
| isContinuityDirectionFlipped | boolean[] | An array whose size is the number of B-Rep edges in the boundary. You can use the getContinuity method to get the list of edges, so you know the number and order of the edges. The isContinuityDirectionFlipped array defines which of the two faces the edge connects to and is used in computing the continuity direction. If the continuity is ConnectedSurfaceContinuityType, or the edge is an open edge and only connected to a single face, the value is ignored. If false, the face associated with the first co-edge returned by the edge is used. |

## Version

Introduced in version November 2022  

