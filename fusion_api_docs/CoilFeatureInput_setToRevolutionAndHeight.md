# CoilFeatureInput.setToRevolutionAndHeight Method

Parent Object: [CoilFeatureInput](CoilFeatureInput.md)  

## Description

Sets the coil type to RevolutionsAndHeightCoilType.

## Syntax

"coilFeatureInput_var" is a variable referencing a [CoilFeatureInput](CoilFeatureInput.md) object.

```python
returnValue = coilFeatureInput_var.setToRevolutionAndHeight(revolutions, height, angle)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| revolutions | [ValueInput](ValueInput.md) | A ValueInput object that defines the number of revolutions. |
| height | [ValueInput](ValueInput.md) | A ValueInput object that defines the height. |
| angle | [ValueInput](ValueInput.md) | A ValueInput object that defines angle. |

## Version

Introduced in version March 2016  

