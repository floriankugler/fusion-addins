# ScaleFeatures.add Method

Parent Object: [ScaleFeatures](ScaleFeatures.md)  

## Description

Creates a new scale feature.

## Syntax

"scaleFeatures_var" is a variable referencing a [ScaleFeatures](ScaleFeatures.md) object.

```python
returnValue = scaleFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [ScaleFeature](ScaleFeature.md) | Returns the newly created ScaleFeature object or null if the creation failed. Returns nothing in the case where the feature is non-parametric. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ScaleFeatureInput](ScaleFeatureInput.md) | A ScaleFeatureInput object that defines the desired scale. Use the createInput method to create a new ScaleFeatureInput object and then use methods on it (the ScaleFeatureInput object) to define the scale. |

## Samples

| Name | Description |
|----|----|
| [scaleFeatures.add](scaleFeatures_add_Sample.md) | Demonstrates the creation a scale feature. |
| [Scale Feature API Sample](ScaleFeatureSample_Sample.md) | Demonstrates creating a new scale feature. |

## Version

Introduced in version January 2015  

