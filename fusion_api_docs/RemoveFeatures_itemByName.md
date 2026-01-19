# RemoveFeatures.itemByName Method

Parent Object: [RemoveFeatures](RemoveFeatures.md)  

## Description

Function that returns the specified remove feature using the name of the feature.

## Syntax

"removeFeatures_var" is a variable referencing a [RemoveFeatures](RemoveFeatures.md) object.

```python
returnValue = removeFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [RemoveFeature](RemoveFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

