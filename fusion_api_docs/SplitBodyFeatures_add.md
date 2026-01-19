# SplitBodyFeatures.add Method

Parent Object: [SplitBodyFeatures](SplitBodyFeatures.md)  

## Description

Creates a new split body feature.

## Syntax

"splitBodyFeatures_var" is a variable referencing a [SplitBodyFeatures](SplitBodyFeatures.md) object.

```python
returnValue = splitBodyFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [SplitBodyFeature](SplitBodyFeature.md) | Returns the newly created SplitBodyFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [SplitBodyFeatureInput](SplitBodyFeatureInput.md) | A SplitBodyFeatureInput object that defines the desired split body feature. Use the createInput method to create a new SplitBodyFeatureInput object and then use methods on it (the SplitBodyFeatureInput object) to define the split body. |

## Samples

| Name | Description |
|----|----|
| [splitBodyFeatures.add](splitBodyfeatures_add_Sample.md) | Demonstrates the splitBodyFeatures.add method. |
| [Split Body Feature API Sample](SplitBodyFeatureSample_Sample.md) | Demonstrates creating a new split body feature. |

## Version

Introduced in version June 2015  

