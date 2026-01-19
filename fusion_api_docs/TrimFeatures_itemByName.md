# TrimFeatures.itemByName Method

Parent Object: [TrimFeatures](TrimFeatures.md)  

## Description

Function that returns the specified trim feature using the name of the feature.

## Syntax

"trimFeatures_var" is a variable referencing a [TrimFeatures](TrimFeatures.md) object.

```python
returnValue = trimFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [TrimFeature](TrimFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

