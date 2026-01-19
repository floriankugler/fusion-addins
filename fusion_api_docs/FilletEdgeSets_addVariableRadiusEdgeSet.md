# FilletEdgeSets.addVariableRadiusEdgeSet Method

Parent Object: [FilletEdgeSets](FilletEdgeSets.md)  

## Description

Adds a single edge or set of tangent edges along with variable radius information to this fillet feature.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"filletEdgeSets_var" is a variable referencing a [FilletEdgeSets](FilletEdgeSets.md) object.

```python
returnValue = filletEdgeSets_var.addVariableRadiusEdgeSet(tangentEdges, startRadius, endRadius, positions, radii, isTangentChain)
```

## Return Value

| Type | Description |
|----|----|
| [VariableRadiusFilletEdgeSet](VariableRadiusFilletEdgeSet.md) | Returns the newly created FilletEdgeSet. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| tangentEdges | [ObjectCollection](ObjectCollection.md) | An object collection containing a single edge or multiple edges. Multiple edges must be tangentially connected and added to the collection in their connected order. If a single edge is input, you can use the isTangentChain argument to automatically find any tangentially connected edges. |
| startRadius | [ValueInput](ValueInput.md) | A ValueInput object that defines the starting radius of the fillet. If a single edge is being filleted, the start radius is at the start end of the edge. If multiple tangent edges are being filleted the start radius is the open end of the first edge in the collection. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| endRadius | [ValueInput](ValueInput.md) | A ValueInput object that defines the ending radius of the fillet. If a single edge is being filleted, the end radius is at the end of the edge. If multiple tangent edges are being filleted the end radius is the open end of the last edge in the collection. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| positions | ValueInput[] | An array of ValueInput objects that defines the positions of any additional radii along the edge(s). The value must be between 0 and 1 and defines the percentage along the curve where a radius is defined. The value is unitless. This array must have the same number of values as the array passed in for the radii argument. |
| radii | ValueInput[] | An array of ValueInput objects that define the radii at positions along the edge(s). This array must have the same number of values as the array passed in for the positions argument. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in"). If no units are specified it will be interpreted using the current default units for length. |
| isTangentChain | boolean | A boolean value for setting whether or not edges that are tangentially connected to the single input edge will also be filleted. |

## Version

Introduced in version November 2022  

