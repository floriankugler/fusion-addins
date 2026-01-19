# ExtrudeFeatures.itemByName Method

Parent Object: [ExtrudeFeatures](ExtrudeFeatures.md)  

## Description

Function that returns the specified extrude feature using the name of the feature.

## Syntax

"extrudeFeatures_var" is a variable referencing an [ExtrudeFeatures](ExtrudeFeatures.md) object.

```python
returnValue = extrudeFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ExtrudeFeature](ExtrudeFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

