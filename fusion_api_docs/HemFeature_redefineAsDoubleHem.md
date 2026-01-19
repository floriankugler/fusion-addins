# HemFeature.redefineAsDoubleHem Method

Parent Object: [HemFeature](HemFeature.md)  

## Description

Redefines the hem as a double hem.

## Syntax

"hemFeature_var" is a variable referencing a [HemFeature](HemFeature.md) object.

```python
returnValue = hemFeature_var.redefineAsDoubleHem(gap, length, setback, isFlipped, bendPositionType)
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if defining the hem is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| gap | [ValueInput](ValueInput.md) | The gap distance of the hem. |
| length | [ValueInput](ValueInput.md) | The length of the double hem. |
| setback | [ValueInput](ValueInput.md) | The setback of the double hem. |
| isFlipped | boolean | Indicates if the hem direction is flipped. |
| bendPositionType | [BendPositionTypes](BendPositionTypes.md) | The bend location type for the hem. |

## Version

Introduced in version September 2025  

