# MoveFeatures.itemByName Method

Parent Object: [MoveFeatures](MoveFeatures.md)  

## Description

Function that returns the specified move feature using the name of the feature.

## Syntax

"moveFeatures_var" is a variable referencing a [MoveFeatures](MoveFeatures.md) object.

```python
returnValue = moveFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [MoveFeature](MoveFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

