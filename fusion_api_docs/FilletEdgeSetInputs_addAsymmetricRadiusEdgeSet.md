# FilletEdgeSetInputs.addAsymmetricRadiusEdgeSet Method

Parent Object: [FilletEdgeSetInputs](FilletEdgeSetInputs.md)  

## Description

Adds an asymmetric fillet edge set to the fillet feature input. Some settings are initialized with a default value and can be set by modifying properties on the returned AsymmetricFilletEdgeSetInput object.

## Syntax

"filletEdgeSetInputs_var" is a variable referencing a [FilletEdgeSetInputs](FilletEdgeSetInputs.md) object.

```python
returnValue = filletEdgeSetInputs_var.addAsymmetricRadiusEdgeSet(entities, offsetOne, offsetTwo, isTangentChain)
```

## Return Value

| Type | Description |
|----|----|
| [AsymmetricFilletEdgeSetInput](AsymmetricFilletEdgeSetInput.md) | Returns the newly created AsymmetricFilletEdgeSetInput. This object provides access to additional settings. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entities | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the BRepEdge, BRepFace, and Feature objects to be filleted. If the isTangentChain argument is true additional edges or faces may also get filleted if they are tangentially connected to any of the input edges or faces. |
| offsetOne | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset of the fillet in the first direction. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| offsetTwo | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset of the fillet in the second direction. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| isTangentChain | boolean | A boolean value for setting whether or not edges or faces that are tangentially connected to the input edges or faces will also be filleted. |

## Version

Introduced in version November 2025  

