# LoftFeatures.add Method

Parent Object: [LoftFeatures](LoftFeatures.md)  

## Description

Creates a new loft feature.

## Syntax

"loftFeatures_var" is a variable referencing a [LoftFeatures](LoftFeatures.md) object.

```python
returnValue = loftFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [LoftFeature](LoftFeature.md) | Returns the newly created LoftFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [LoftFeatureInput](LoftFeatureInput.md) | A LoftFeatureInput object that defines the desired loft feature. Use the createInput method to create a new LoftFeatureInput object and then use methods on it (the LoftFeatureInput object) to define the required input. |

## Samples

| Name | Description |
|----|----|
| [loftFeatures.add](loftFeatures_add_Sample.md) | Demonstrates the loftFeatures.add method. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version August 2016  

