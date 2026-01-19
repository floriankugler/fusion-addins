# ReplaceFaceFeatures.add Method

Parent Object: [ReplaceFaceFeatures](ReplaceFaceFeatures.md)  

## Description

Creates a new replace face feature.

## Syntax

"replaceFaceFeatures_var" is a variable referencing a [ReplaceFaceFeatures](ReplaceFaceFeatures.md) object.

```python
returnValue = replaceFaceFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [ReplaceFaceFeature](ReplaceFaceFeature.md) | Returns the newly created ReplaceFaceFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ReplaceFaceFeatureInput](ReplaceFaceFeatureInput.md) | A ReplaceFaceFeatureInput object that defines the desired replace face. Use the createInput method to create a new ReplaceFaceFeatureInput object and then use methods on it (the ReplaceFaceFeatureInput object) to define the replace face. |

## Samples

| Name | Description |
|----|----|
| [replaceFaceFeatures.add](replaceFaceFeatures_add_Sample.md) | Demonstrate the remove replaceFaceFeatures.add method. |
| [ReplaceFace Feature](ReplaceFaceFeatureSample_Sample.md) | Demonstrates creating a new replaceface feature. |

## Version

Introduced in version March 2015  

