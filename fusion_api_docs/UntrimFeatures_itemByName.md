# UntrimFeatures.itemByName Method

Parent Object: [UntrimFeatures](UntrimFeatures.md)  

## Description

Function that returns the specified Untrim feature using the name of the feature.

## Syntax

"untrimFeatures_var" is a variable referencing a [UntrimFeatures](UntrimFeatures.md) object.

```python
returnValue = untrimFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [UntrimFeature](UntrimFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version January 2021  

