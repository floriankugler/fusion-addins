# MergeFacesFeatures.add Method

Parent Object: [MergeFacesFeatures](MergeFacesFeatures.md)  

## Description

Creates a new merge face feature.

## Syntax

"mergeFacesFeatures_var" is a variable referencing a [MergeFacesFeatures](MergeFacesFeatures.md) object.

```python
returnValue = mergeFacesFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if successful. Because this is limited to direct modelling only that directly modifies the B-Rep body and does not create a MergeFacesFeature object there is nothing to return besides if the merge was successful or no. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [MergeFacesFeatureInput](MergeFacesFeatureInput.md) | A MergeFacesFeatureInput object that defines the desired merge. Use the createInput method to create a new MergeFacesFeatureInput object and then use methods on it (the MergeFacesFeatureInput object) to define the merge. |

## Version

Introduced in version September 2024  

