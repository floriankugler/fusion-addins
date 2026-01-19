# SplitFaceFeatures.add Method

Parent Object: [SplitFaceFeatures](SplitFaceFeatures.md)  

## Description

Creates a new split face feature.

## Syntax

"splitFaceFeatures_var" is a variable referencing a [SplitFaceFeatures](SplitFaceFeatures.md) object.

```python
returnValue = splitFaceFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [SplitFaceFeature](SplitFaceFeature.md) | Returns the newly created SplitFaceFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [SplitFaceFeatureInput](SplitFaceFeatureInput.md) | A SplitFaceFeatureInput object that defines the desired split face feature. Use the createInput method to create a new SplitFaceFeatureInput object and then use methods on it (the SplitFaceFeatureInput object) to define the split face. |

## Samples

| Name | Description |
|----|----|
| [splitFaceFeatures.add](splitFaceFeatures_add_Sample.md) | Demonstrates the splitFaceFeatures.add method by spliting a face with another intersecting face. |
| [Split Face Feature API Sample](SplitFaceFeatureSample_Sample.md) | Demonstrates creating a new split face feature. |

## Version

Introduced in version June 2015  

