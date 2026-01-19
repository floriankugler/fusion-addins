# ScaleFeatureInput.setToNonUniform Method

Parent Object: [ScaleFeatureInput](ScaleFeatureInput.md)  

## Description

Sets the scale factor for the x, y, z directions to define a non-uniform scale. Calling this method will cause the isUniform property to be set to false. This will fail if the inputEntities collection contains sketches or components.

## Syntax

"scaleFeatureInput_var" is a variable referencing a [ScaleFeatureInput](ScaleFeatureInput.md) object.

```python
returnValue = scaleFeatureInput_var.setToNonUniform(xScale, yScale, zScale)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| xScale | [ValueInput](ValueInput.md) | A ValueInput object that defines the scale in the X direction. |
| yScale | [ValueInput](ValueInput.md) | A ValueInput object that defines the scale in the Y direction. |
| zScale | [ValueInput](ValueInput.md) | A ValueInput object that defines the scale in the Z direction. |

## Samples

| Name | Description |
|----|----|
| [Scale Feature API Sample](ScaleFeatureSample_Sample.md) | Demonstrates creating a new scale feature. |

## Version

Introduced in version January 2015  

