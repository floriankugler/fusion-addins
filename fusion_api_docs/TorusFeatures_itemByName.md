# TorusFeatures.itemByName Method

Parent Object: [TorusFeatures](TorusFeatures.md)  

## Description

Function that returns the specified torus feature using the name of the feature.

## Syntax

"torusFeatures_var" is a variable referencing a [TorusFeatures](TorusFeatures.md) object.

```python
returnValue = torusFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [TorusFeature](TorusFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

