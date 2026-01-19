# DeriveFeatures.add Method

Parent Object: [DeriveFeatures](DeriveFeatures.md)  

## Description

Creates a new derive feature.

## Syntax

"deriveFeatures_var" is a variable referencing a [DeriveFeatures](DeriveFeatures.md) object.

```python
returnValue = deriveFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [DeriveFeature](DeriveFeature.md) | Returns the newly created DeriveFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [DeriveFeatureInput](DeriveFeatureInput.md) | A DeriveFeatureInput object that defines the desired derive. Use the createInput method to create a new DeriveFeatureInput object and then use methods on it to define the derive. |

## Version

Introduced in version January 2026  

