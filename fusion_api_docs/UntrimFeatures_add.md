# UntrimFeatures.add Method

Parent Object: [UntrimFeatures](UntrimFeatures.md)  

## Description

Creates a new Untrim feature.

## Syntax

"untrimFeatures_var" is a variable referencing a [UntrimFeatures](UntrimFeatures.md) object.

```python
returnValue = untrimFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [UntrimFeature](UntrimFeature.md) | Returns the newly created UntrimFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [UntrimFeatureInput](UntrimFeatureInput.md) | An UntrimFeatureInput object that defines the desired Untrim feature. Use the createInput method to create a new UntrimFeatureInput object and then use methods on it (the UntrimFeatureInput object) to define the desired options for the Untrim feature. |

## Samples

| Name | Description |
|----|----|
| [Untrim Feature API Sample](UntrimFeatureSample_Sample.md) | Demonstrates creating a new untrim feature. |

## Version

Introduced in version January 2021  

