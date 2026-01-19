# MirrorFeatures.itemByName Method

Parent Object: [MirrorFeatures](MirrorFeatures.md)  

## Description

Function that returns the specified mirror feature using the name of the feature.

## Syntax

"mirrorFeatures_var" is a variable referencing a [MirrorFeatures](MirrorFeatures.md) object.

```python
returnValue = mirrorFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [MirrorFeature](MirrorFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

