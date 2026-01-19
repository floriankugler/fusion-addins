# ChamferEdgeSets.addTwoDistancesChamferEdgeSet Method

Parent Object: [ChamferEdgeSets](ChamferEdgeSets.md)  

## Description

Adds a set of edges an equal distance offset to this chamfer feature.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"chamferEdgeSets_var" is a variable referencing a [ChamferEdgeSets](ChamferEdgeSets.md) object.

```python
returnValue = chamferEdgeSets_var.addTwoDistancesChamferEdgeSet(edges, distanceOne, distanceTwo, isFlipped, isTangentChain)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the set of edges was successfully added to the ChamferFeatureInput. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edges | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the edges to be chamfered. Edges can be defined by passing in BrepEdge, BRepFace, or Feature objects. If BRepFace or Feature objects are passed in all of the edges associated with those objects will be chamfered. If BRepEdge objects are provided and the isTangentChain argument is true additional edges may also get chamfered if they are tangentially connected to any of the input edges. |
| distanceOne | [ValueInput](ValueInput.md) | A ValueInput object that defines the first distance offset of the chamfer. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| distanceTwo | [ValueInput](ValueInput.md) | A ValueInput object that defines the second distance offset of the chamfer. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| isFlipped | boolean | Swaps the directions for distance one and two. |
| isTangentChain | boolean | A boolean value for setting whether or not edges that are tangentially connected to the input edges (if any) will also be chamfered. |

## Version

Introduced in version December 2020  

