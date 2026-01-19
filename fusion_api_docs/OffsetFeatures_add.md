# OffsetFeatures.add Method

Parent Object: [OffsetFeatures](OffsetFeatures.md)  

## Description

Creates a new offset feature.

## Syntax

"offsetFeatures_var" is a variable referencing an [OffsetFeatures](OffsetFeatures.md) object.

```python
returnValue = offsetFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetFeature](OffsetFeature.md) | Returns the newly created OffsetFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [OffsetFeatureInput](OffsetFeatureInput.md) | A FeatureInput object that defines the desired offset feature. Use the createInput method to create a new OffsetFeatureInput object and then use methods on it (the OffsetFeatureInput object) to define the offset feature. |

## Samples

| Name | Description |
|----|----|
| [offsetFeatures.add](offsetFeatures_add_Sample.md) | Demonstrates the offsetFeatures.add method. This is the equivalent of the Offset command in the SURFACE tab. |
| [Offset Feature API Sample](OffsetFeatureSample_Sample.md) | Demonstrates creating a new offset feature |

## Version

Introduced in version June 2015  

