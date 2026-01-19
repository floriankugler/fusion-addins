# UnfoldFeatures.itemByName Method

Parent Object: [UnfoldFeatures](UnfoldFeatures.md)  

## Description

Function that returns the specified unfold feature using the name of the feature.

## Syntax

"unfoldFeatures_var" is a variable referencing a [UnfoldFeatures](UnfoldFeatures.md) object.

```python
returnValue = unfoldFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [UnfoldFeature](UnfoldFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version August 2020  

