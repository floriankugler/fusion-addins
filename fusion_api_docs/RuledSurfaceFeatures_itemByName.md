# RuledSurfaceFeatures.itemByName Method

Parent Object: [RuledSurfaceFeatures](RuledSurfaceFeatures.md)  

## Description

Function that returns the specified RuledSurface feature using the name of the feature.

## Syntax

"ruledSurfaceFeatures_var" is a variable referencing a [RuledSurfaceFeatures](RuledSurfaceFeatures.md) object.

```python
returnValue = ruledSurfaceFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [RuledSurfaceFeature](RuledSurfaceFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2020  

