# HemFeature.redefineAsRolledHem Method

Parent Object: [HemFeature](HemFeature.md)  

## Description

Redefines the hem as a rolled hem.

## Syntax

"hemFeature_var" is a variable referencing a [HemFeature](HemFeature.md) object.

```python
returnValue = hemFeature_var.redefineAsRolledHem(radius, angle, isFlipped, bendPositionType)
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if defining the hem is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| radius | [ValueInput](ValueInput.md) | The radius of the rolled hem. |
| angle | [ValueInput](ValueInput.md) | The angle of the rolled hem. |
| isFlipped | boolean | Indicates if the hem direction is flipped. |
| bendPositionType | [BendPositionTypes](BendPositionTypes.md) | The bend location type for the hem. |

## Version

Introduced in version September 2025  

