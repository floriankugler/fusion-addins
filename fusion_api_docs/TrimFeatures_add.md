# TrimFeatures.add Method

Parent Object: [TrimFeatures](TrimFeatures.md)  

## Description

Creates a new trim feature.

## Syntax

"trimFeatures_var" is a variable referencing a [TrimFeatures](TrimFeatures.md) object.

```python
returnValue = trimFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [TrimFeature](TrimFeature.md) | Returns the newly created TrimFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [TrimFeatureInput](TrimFeatureInput.md) | A TrimFeatureInput object that defines the desired trim feature. Use the createInput method to create a new TrimFeatureInput object and then use methods on it (the TrimFeatureInput object) to define the trim feature. |

## Samples

| Name | Description |
|----|----|
| [trimFeatures.add](trimFeatures_add_Sample.md) | Demonstrates the trimFeatures.add method. |
| [Trim Feature API Sample](TrimFeatureSample_Sample.md) | Demonstrates creating a new trim feature. |

## Version

Introduced in version July 2015  

