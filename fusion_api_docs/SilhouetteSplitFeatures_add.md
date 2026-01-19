# SilhouetteSplitFeatures.add Method

Parent Object: [SilhouetteSplitFeatures](SilhouetteSplitFeatures.md)  

## Description

Creates a new silhouette split feature.

## Syntax

"silhouetteSplitFeatures_var" is a variable referencing a [SilhouetteSplitFeatures](SilhouetteSplitFeatures.md) object.

```python
returnValue = silhouetteSplitFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [SilhouetteSplitFeature](SilhouetteSplitFeature.md) | Returns the newly created SilhouetteSplitFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [SilhouetteSplitFeatureInput](SilhouetteSplitFeatureInput.md) | A SilhouetteSplitFeatureInput object that defines the desired silhouette split feature. Use the createInput method to create a new SilhouetteSplitFeatureInput object and then use methods on it (the SilhouetteSplitFeatureInput object) to define the silhouette split. |

## Samples

| Name | Description |
|----|----|
| [silhouetteSplitFeatures.add](silhouetteSplitFeatures_add_Sample.md) | Demonstrates the silhouetteSplitFeatures.add method. The Silhouette Split feature is limited in the bodies it will split. The simplest body to get a valid result is to create a sphere and split it. |
| [Silhouette Split Feature API Sample](SilhouetteSplitFeatureSample_Sample.md) | Demonstrates creating a new silhouette split feature. |

## Version

Introduced in version June 2015  

