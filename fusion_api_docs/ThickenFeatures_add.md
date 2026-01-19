# ThickenFeatures.add Method

Parent Object: [ThickenFeatures](ThickenFeatures.md)  

## Description

Creates a new Thicken feature.

## Syntax

"thickenFeatures_var" is a variable referencing a [ThickenFeatures](ThickenFeatures.md) object.

```python
returnValue = thickenFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [ThickenFeature](ThickenFeature.md) | Returns the newly created ThickenFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ThickenFeatureInput](ThickenFeatureInput.md) | A FeatureInput object that defines the desired Thicken feature. Use the createInput method to create a new ThickenFeatureInput object and then use methods on it (the ThickenFeatureInput object) to define the Thicken feature. |

## Samples

| Name | Description |
|----|----|
| [thickenFeatures.add](thickenFeatures_add_Sample.md) | Demonstrates the thickenFeatures.add method. |
| [Thicken Feature API Sample](ThickenFeatureSample_Sample.md) | Demonstrates creating a new thiken feature. |

## Version

Introduced in version June 2015  

