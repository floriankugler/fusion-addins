# CoilFeatureInput.setToHeightAndPitchCoil Method

Parent Object: [CoilFeatureInput](CoilFeatureInput.md)  

## Description

Sets the coil type to HeightAndPitchCoilType.

## Syntax

"coilFeatureInput_var" is a variable referencing a [CoilFeatureInput](CoilFeatureInput.md) object.

```python
returnValue = coilFeatureInput_var.setToHeightAndPitchCoil(height, pitch, angle)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| height | [ValueInput](ValueInput.md) | A ValueInput object that defines the height. |
| pitch | [ValueInput](ValueInput.md) | A ValueInput object that defines the pitch. |
| angle | [ValueInput](ValueInput.md) | A ValueInput object that defines angle. |

## Version

Introduced in version March 2016  

