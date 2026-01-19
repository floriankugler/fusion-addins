# RipFeatures.itemByName Method

Parent Object: [RipFeatures](RipFeatures.md)  

## Description

Function that returns the specified Rip feature using the name of the feature.

## Syntax

"ripFeatures_var" is a variable referencing a [RipFeatures](RipFeatures.md) object.

```python
returnValue = ripFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [RipFeature](RipFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2023  

