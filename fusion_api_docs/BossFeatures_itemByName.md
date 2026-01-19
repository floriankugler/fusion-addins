# BossFeatures.itemByName Method

Parent Object: [BossFeatures](BossFeatures.md)  

## Description

Function that returns the specified boss feature using the name of the feature.

## Syntax

"bossFeatures_var" is a variable referencing a [BossFeatures](BossFeatures.md) object.

```python
returnValue = bossFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [BossFeature](BossFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version October 2022  

