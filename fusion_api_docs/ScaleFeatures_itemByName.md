# ScaleFeatures.itemByName Method

Parent Object: [ScaleFeatures](ScaleFeatures.md)  

## Description

Function that returns the specified scale feature using the name of the feature.

## Syntax

"scaleFeatures_var" is a variable referencing a [ScaleFeatures](ScaleFeatures.md) object.

```python
returnValue = scaleFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ScaleFeature](ScaleFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

