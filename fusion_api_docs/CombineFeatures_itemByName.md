# CombineFeatures.itemByName Method

Parent Object: [CombineFeatures](CombineFeatures.md)  

## Description

Function that returns the specified combine feature using the name of the feature.

## Syntax

"combineFeatures_var" is a variable referencing a [CombineFeatures](CombineFeatures.md) object.

```python
returnValue = combineFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [CombineFeature](CombineFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

