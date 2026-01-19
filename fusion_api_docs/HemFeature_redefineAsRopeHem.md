# HemFeature.redefineAsRopeHem Method

Parent Object: [HemFeature](HemFeature.md)  

## Description

Redefines the hem as a rope hem.

## Syntax

"hemFeature_var" is a variable referencing a [HemFeature](HemFeature.md) object.

```python
returnValue = hemFeature_var.redefineAsRopeHem(length, gap, radius, isFlipped, bendPositionType)
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if defining the hem is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| length | [ValueInput](ValueInput.md) | The length of the rope hem. |
| gap | [ValueInput](ValueInput.md) | The gap distance of the hem. |
| radius | [ValueInput](ValueInput.md) | The radius of the rope hem. |
| isFlipped | boolean | Indicates if the hem direction is flipped. |
| bendPositionType | [BendPositionTypes](BendPositionTypes.md) | The bend location type for the hem. |

## Version

Introduced in version September 2025  

