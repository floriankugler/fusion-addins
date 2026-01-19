# OffsetFacesFeatures.add Method

Parent Object: [OffsetFacesFeatures](OffsetFacesFeatures.md)  

## Description

Creates a new offset feature.

## Syntax

"offsetFacesFeatures_var" is a variable referencing an [OffsetFacesFeatures](OffsetFacesFeatures.md) object.

```python
returnValue = offsetFacesFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetFacesFeature](OffsetFacesFeature.md) | Returns the newly created OffsetFacesFeature object or null if the creation failed. Returns nothing in the case where the feature is non-parametric. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [OffsetFacesFeatureInput](OffsetFacesFeatureInput.md) | An OffsetFacesFeatureInput object that defines the desired offset faces feature. Use the createInput method to create a new OffsetFacesFeatureInput object and then use methods on it (the OffsetFacesFeatureInput object) to define the offset feature. |

## Version

Introduced in version November 2025  

