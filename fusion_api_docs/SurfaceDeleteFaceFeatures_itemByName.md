# SurfaceDeleteFaceFeatures.itemByName Method

Parent Object: [SurfaceDeleteFaceFeatures](SurfaceDeleteFaceFeatures.md)  

## Description

Function that returns the specified SurfaceDeleteFaceFeature object using the name of the feature.

## Syntax

"surfaceDeleteFaceFeatures_var" is a variable referencing a [SurfaceDeleteFaceFeatures](SurfaceDeleteFaceFeatures.md) object.

```python
returnValue = surfaceDeleteFaceFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [SurfaceDeleteFaceFeature](SurfaceDeleteFaceFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version August 2016  

