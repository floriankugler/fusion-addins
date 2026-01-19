# ThreadFeatures.add Method

Parent Object: [ThreadFeatures](ThreadFeatures.md)  

## Description

Creates a new thread feature.

## Syntax

"threadFeatures_var" is a variable referencing a [ThreadFeatures](ThreadFeatures.md) object.

```python
returnValue = threadFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [ThreadFeature](ThreadFeature.md) | Returns the newly created ThreadFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ThreadFeatureInput](ThreadFeatureInput.md) | A ThreadFeatureInput object that defines the desired thread. Use the createInput method to create a new ThreadFeatureInput object and then use methods on it (the ThreadFeatureInput object) to define the thread. |

## Samples

| Name | Description |
|----|----|
| [Thread Feature API Sample](ThreadFeatureSample_Sample.md) | Demonstrates creating a new thread feature. |

## Version

Introduced in version January 2015  

