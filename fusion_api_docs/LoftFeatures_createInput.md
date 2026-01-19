# LoftFeatures.createInput Method

Parent Object: [LoftFeatures](LoftFeatures.md)  

## Description

Creates a LoftFeatureInput object. Use properties and methods on the returned LoftFeatureInput object to provide the required input to create a loft feature. The LoftFeatureInput object can then be used as input to the add method to create the loft feature.

## Syntax

"loftFeatures_var" is a variable referencing a [LoftFeatures](LoftFeatures.md) object.

```python
returnValue = loftFeatures_var.createInput(operation)
```

## Return Value

| Type | Description |
|----|----|
| [LoftFeatureInput](LoftFeatureInput.md) | Returns the newly created LoftFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| operation | [FeatureOperations](FeatureOperations.md) | The feature operation to perform. |

## Samples

| Name | Description |
|----|----|
| [loftFeatures.add](loftFeatures_add_Sample.md) | Demonstrates the loftFeatures.add method. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version August 2016  

