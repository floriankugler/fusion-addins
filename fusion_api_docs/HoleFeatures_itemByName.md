# HoleFeatures.itemByName Method

Parent Object: [HoleFeatures](HoleFeatures.md)  

## Description

Function that returns the specified hole feature using the name of the feature.

## Syntax

"holeFeatures_var" is a variable referencing a [HoleFeatures](HoleFeatures.md) object.

```python
returnValue = holeFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [HoleFeature](HoleFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

