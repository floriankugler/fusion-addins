# ExtendFeatures.add Method

Parent Object: [ExtendFeatures](ExtendFeatures.md)  

## Description

Creates a new extend feature.

## Syntax

"extendFeatures_var" is a variable referencing an [ExtendFeatures](ExtendFeatures.md) object.

```python
returnValue = extendFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [ExtendFeature](ExtendFeature.md) | Returns the newly created ExtendFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ExtendFeatureInput](ExtendFeatureInput.md) | An ExtendFeatureInput object that defines the desired extend feature. Use the createInput method to create a new ExtendFeatureInput object and then use methods on it (the ExtendFeatureInput object) to define the desired options for the extent feature. |

## Samples

| Name | Description |
|----|----|
| [extendFeatures.add](extendFeatures_add_Sample.md) | Demonstrates the extendFeatures.add method. To use this sample, have a design open that contains at least one surface body. When you run the sample, you will be prompted to select an open edge of the body. |

## Version

Introduced in version June 2015  

