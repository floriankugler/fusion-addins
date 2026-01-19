# FilletEdgeSets.addAsymmetricRadiusEdgeSet Method

Parent Object: [FilletEdgeSets](FilletEdgeSets.md)  

## Description

Adds an asymmetric fillet edge set to the fillet feature.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"filletEdgeSets_var" is a variable referencing a [FilletEdgeSets](FilletEdgeSets.md) object.

```python
returnValue = filletEdgeSets_var.addAsymmetricRadiusEdgeSet(entities, offsetOne, offsetTwo, isTangentChain)
```

## Return Value

| Type | Description |
|----|----|
| [AsymmetricFilletEdgeSet](AsymmetricFilletEdgeSet.md) | Returns the newly created AsymmetricFilletEdgeSet. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entities | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the BRepEdge, BRepFace, and Feature objects to be filleted. If the isTangentChain argument is true additional edges or faces may also get filleted if they are tangentially connected to any of the input edges or faces. |
| offsetOne | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset distance of the fillet in the first direction. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| offsetTwo | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset distance of the fillet in the second direction. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| isTangentChain | boolean | A boolean value for setting whether or not edges or faces that are tangentially connected to the input edges or faces will also be filleted. |

## Version

Introduced in version November 2025  

