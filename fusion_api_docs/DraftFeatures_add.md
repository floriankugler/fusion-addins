# DraftFeatures.add Method

Parent Object: [DraftFeatures](DraftFeatures.md)  

## Description

Creates a new draft feature.

## Syntax

"draftFeatures_var" is a variable referencing a [DraftFeatures](DraftFeatures.md) object.

```python
returnValue = draftFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [DraftFeature](DraftFeature.md) | Returns the newly created DraftFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [DraftFeatureInput](DraftFeatureInput.md) | A DraftFeatureInput object that defines the desired draft. Use the createInput method to create a new DraftFeatureInput object and then use methods on it (the DraftFeatureInput object) to define the draft. |

## Samples

| Name | Description |
|----|----|
| [draftFeatures.add](draftFeatures_add_Sample.md) | Demonstrates the draftFeatures.add method. To use this sample, have a design open that contains at least one body. When you run the sample, you will be prompted to select the face to draft. Because the pull direction is using the base X-Y plane, you need to select a face that is not parallel to the X-Y plane. |
| [Draft Feature API Sample](DraftFeatureSample_Sample.md) | Demonstrates creating a new draft feature. |

## Version

Introduced in version January 2015  

