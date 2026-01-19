# HemFeature.redefineAsTeardropHem Method

Parent Object: [HemFeature](HemFeature.md)  

## Description

Redefines the hem as a teardrop hem.

## Syntax

"hemFeature_var" is a variable referencing a [HemFeature](HemFeature.md) object.

```python
returnValue = hemFeature_var.redefineAsTeardropHem(radius, length, gap, isFlipped, bendPositionType)
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if defining the hem is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| radius | [ValueInput](ValueInput.md) | The radius of the teardrop hem. |
| length | [ValueInput](ValueInput.md) | The length of the teardrop hem. |
| gap | [ValueInput](ValueInput.md) | The gap distance of the hem. |
| isFlipped | boolean | Indicates if the hem direction is flipped. |
| bendPositionType | [BendPositionTypes](BendPositionTypes.md) | The bend location type for the hem. |

## Version

Introduced in version September 2025  

