# ThickenFeatures.itemByName Method

Parent Object: [ThickenFeatures](ThickenFeatures.md)  

## Description

Function that returns the specified thicken feature using the name of the feature.

## Syntax

"thickenFeatures_var" is a variable referencing a [ThickenFeatures](ThickenFeatures.md) object.

```python
returnValue = thickenFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ThickenFeature](ThickenFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

