# MoveFeatureInput.defineAsTranslateXYZ Method

Parent Object: [MoveFeatureInput](MoveFeatureInput.md)  

## Description

This method will define a move feature that defines a translation in X, Y, and Z.

## Syntax

"moveFeatureInput_var" is a variable referencing a [MoveFeatureInput](MoveFeatureInput.md) object.

```python
returnValue = moveFeatureInput_var.defineAsTranslateXYZ(xDistance, yDistance, zDistance, isDesignSpace)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | Returns true if defining the type of move is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| xDistance | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset in the X direction. If the ValueInput is created using a real value, the distance is in centimeters. If it's defined using a string, the default document units are used. |
| yDistance | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset in the Y direction. If the ValueInput is created using a real value, the distance is in centimeters. If it's defined using a string, the default document units are used. |
| zDistance | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset in the Z direction. If the ValueInput is created using a real value, the distance is in centimeters. If it's defined using a string, the default document units are used. |
| isDesignSpace | boolean | Defines if the translation is defined with respect to the design or component space. Design space is the same as the root component space. |

## Version

Introduced in version January 2023  

