# HoleFeatureInput.setPositionOnEdge Method

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Defines the position and orientation of the hole to be on the start, end or center of an edge.

## Syntax

"holeFeatureInput_var" is a variable referencing a [HoleFeatureInput](HoleFeatureInput.md) object.

```python
returnValue = holeFeatureInput_var.setPositionOnEdge(planarEntity, edge, position)
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

## Samples

| Name | Description |
|----|----|
| [holeFeatures.add with Counterbore](holeFeaturesCounterBore_add_Sample.md) | Demonstrates the holeFeatures.add method using the createCounterboreInput method. The hole is positioned at the center of the selected edge. |

## Version

Introduced in version August 2014  

