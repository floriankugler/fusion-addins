# CoilFeatures.itemByName Method

Parent Object: [CoilFeatures](CoilFeatures.md)  

## Description

Function that returns the specified coil feature using the name of the feature.

## Syntax

"coilFeatures_var" is a variable referencing a [CoilFeatures](CoilFeatures.md) object.

```python
returnValue = coilFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [CoilFeature](CoilFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

