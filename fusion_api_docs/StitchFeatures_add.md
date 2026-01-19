# StitchFeatures.add Method

Parent Object: [StitchFeatures](StitchFeatures.md)  

## Description

Creates a new stitch feature.

## Syntax

"stitchFeatures_var" is a variable referencing a [StitchFeatures](StitchFeatures.md) object.

```python
returnValue = stitchFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [StitchFeature](StitchFeature.md) | Returns the newly created StitchFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [StitchFeatureInput](StitchFeatureInput.md) | A StitchFeatureInput object that defines the desired stitch feature. Use the createInput method to create a new StitchFeatureInput object and then use methods on it (the StitchFeatureInput object) to define the stitch feature. |

## Samples

| Name | Description |
|----|----|
| [stitchFeatures.add](stitchFeatures_add_Sample.md) | Demonstrates the stitchFeatures.add method. |
| [Stitch Feature API Sample](StitchFeatureSample_Sample.md) | Demonstrates creating a new stitch feature. |

## Version

Introduced in version June 2015  

