# BaseFeatures.itemByName Method

Parent Object: [BaseFeatures](BaseFeatures.md)  

## Description

Function that returns the specified base feature using the name of the feature.

## Syntax

"baseFeatures_var" is a variable referencing a [BaseFeatures](BaseFeatures.md) object.

```python
returnValue = baseFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [BaseFeature](BaseFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

