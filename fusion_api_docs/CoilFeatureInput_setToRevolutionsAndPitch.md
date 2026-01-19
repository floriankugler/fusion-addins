# CoilFeatureInput.setToRevolutionsAndPitch Method

Parent Object: [CoilFeatureInput](CoilFeatureInput.md)  

## Description

Sets the coil type to RevolutionsAndPitchCoilType.

## Syntax

"coilFeatureInput_var" is a variable referencing a [CoilFeatureInput](CoilFeatureInput.md) object.

```python
returnValue = coilFeatureInput_var.setToRevolutionsAndPitch(revolutions, pitch, angle)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| revolutions | [ValueInput](ValueInput.md) | A ValueInput object that defines the number of revolutions. |
| pitch | [ValueInput](ValueInput.md) | A ValueInput object that defines the pitch. |
| angle | [ValueInput](ValueInput.md) | A ValueInput object that defines angle. |

## Version

Introduced in version March 2016  

