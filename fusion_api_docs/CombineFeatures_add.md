# CombineFeatures.add Method

Parent Object: [CombineFeatures](CombineFeatures.md)  

## Description

Creates a new combine feature.

## Syntax

"combineFeatures_var" is a variable referencing a [CombineFeatures](CombineFeatures.md) object.

```python
returnValue = combineFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [CombineFeature](CombineFeature.md) | Returns the newly created CombineFeature object or null if the creation failed. This function returns nothing in the case where the feature is non-parametric. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [CombineFeatureInput](CombineFeatureInput.md) | A CombineFeatureInput object that defines the desired combine. Use the createInput method to create a new CombineFeatureInput object and then use methods on it (the CombineFeatureInput object) to define the combine. |

## Samples

| Name | Description |
|----|----|
| [combineFeatures.add](combineFeatures_add_Sample.md) | Demonstrates the combineFeatures.add method. To use this sample, have a design open that contains at least two bodies. When you run the sample, you will be prompted to select the bodies and they will joined. |

## Version

Introduced in version November 2014  

