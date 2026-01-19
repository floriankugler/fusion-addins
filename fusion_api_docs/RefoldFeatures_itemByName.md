# RefoldFeatures.itemByName Method

Parent Object: [RefoldFeatures](RefoldFeatures.md)  

## Description

Function that returns the specified refold feature using the name of the feature.

## Syntax

"refoldFeatures_var" is a variable referencing a [RefoldFeatures](RefoldFeatures.md) object.

```python
returnValue = refoldFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [RefoldFeature](RefoldFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version August 2020  

