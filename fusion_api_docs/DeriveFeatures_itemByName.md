# DeriveFeatures.itemByName Method

Parent Object: [DeriveFeatures](DeriveFeatures.md)  

## Description

Function that returns the specified derive feature using the name of the feature.

## Syntax

"deriveFeatures_var" is a variable referencing a [DeriveFeatures](DeriveFeatures.md) object.

```python
returnValue = deriveFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [DeriveFeature](DeriveFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version January 2026  

