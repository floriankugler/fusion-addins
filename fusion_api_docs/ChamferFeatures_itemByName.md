# ChamferFeatures.itemByName Method

Parent Object: [ChamferFeatures](ChamferFeatures.md)  

## Description

Function that returns the specified chamfer feature using the name of the feature.

## Syntax

"chamferFeatures_var" is a variable referencing a [ChamferFeatures](ChamferFeatures.md) object.

```python
returnValue = chamferFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ChamferFeature](ChamferFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

