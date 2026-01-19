# SweepFeatures.itemByName Method

Parent Object: [SweepFeatures](SweepFeatures.md)  

## Description

Function that returns the specified sweep feature using the name of the feature.

## Syntax

"sweepFeatures_var" is a variable referencing a [SweepFeatures](SweepFeatures.md) object.

```python
returnValue = sweepFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [SweepFeature](SweepFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

