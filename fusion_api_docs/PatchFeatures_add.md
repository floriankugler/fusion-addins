# PatchFeatures.add Method

Parent Object: [PatchFeatures](PatchFeatures.md)  

## Description

Creates a new patch feature.

## Syntax

"patchFeatures_var" is a variable referencing a [PatchFeatures](PatchFeatures.md) object.

```python
returnValue = patchFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [PatchFeature](PatchFeature.md) | Returns the newly created PatchFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [PatchFeatureInput](PatchFeatureInput.md) | A PatchFeatureInput object that defines the desired patch feature. Use the createInput method to create a new PatchFeatureInput object and then use methods on it (the PatchFeatureInput object) to define the patch feature. |

## Samples

| Name | Description |
|----|----|
| [patchFeatures.add](patchFeatures_add_Sample.md) | Demonstrates the patchFeatures.add method by creating a patch surface on the selected profile. |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version July 2016  

