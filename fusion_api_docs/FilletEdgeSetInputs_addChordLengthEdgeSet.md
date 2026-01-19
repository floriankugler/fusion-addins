# FilletEdgeSetInputs.addChordLengthEdgeSet Method

Parent Object: [FilletEdgeSetInputs](FilletEdgeSetInputs.md)  

## Description

Adds a set of edges to be filleted with a chord length fillet to the fillet feature input. Some settings are initialized with a default value and can be set by modifying properties on the returned ChordLengthFilletEdgeSetInput object.

## Syntax

"filletEdgeSetInputs_var" is a variable referencing a [FilletEdgeSetInputs](FilletEdgeSetInputs.md) object.

```python
returnValue = filletEdgeSetInputs_var.addChordLengthEdgeSet(entities, chordLength, isTangentChain)
```

## Return Value

| Type | Description |
|----|----|
| [ChordLengthFilletEdgeSetInput](ChordLengthFilletEdgeSetInput.md) | Returns the newly created ChordLengthFilletEdgeSetInput. This object provides access to additional settings. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entities | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the BRepEdge, BRepFace, and Feature objects to be filleted. If the isTangentChain argument is true additional edges or faces may also get filleted if they are tangentially connected to any of the input edges or faces. |
| chordLength | [ValueInput](ValueInput.md) | A ValueInput object that defines the chord length of the fillet. If the ValueInput uses a real value then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current document units for length. |
| isTangentChain | boolean | A boolean value for setting whether or not edges or faces that are tangentially connected to the input edges or faces (if any) will also be filleted. |

## Samples

| Name | Description |
|----|----|
| [Fillet Feature API Sample](FilletFeatureSample_Sample.md) | Demonstrates creating fillets using the various types of fillets. Create a new design and add a box that is at least 2 cm on each side. The script creates a constant radius, variable radius and chord length fillets. After creating each one, it deletes it and then creates the next. To see any of the fillets that were deleted, undo to get the fillet back. |

## Version

Introduced in version November 2022  

