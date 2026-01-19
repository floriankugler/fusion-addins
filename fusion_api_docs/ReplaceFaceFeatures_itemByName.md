# ReplaceFaceFeatures.itemByName Method

Parent Object: [ReplaceFaceFeatures](ReplaceFaceFeatures.md)  

## Description

Function that returns the specified replace face feature using the name of the feature.

## Syntax

"replaceFaceFeatures_var" is a variable referencing a [ReplaceFaceFeatures](ReplaceFaceFeatures.md) object.

```python
returnValue = replaceFaceFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ReplaceFaceFeature](ReplaceFaceFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

