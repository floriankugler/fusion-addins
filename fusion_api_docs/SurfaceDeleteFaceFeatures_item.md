# SurfaceDeleteFaceFeatures.item Method

Parent Object: [SurfaceDeleteFaceFeatures](SurfaceDeleteFaceFeatures.md)  

## Description

Function that returns the specified SurfaceDeleteFaceFeature object using an index into the collection.

## Syntax

"surfaceDeleteFaceFeatures_var" is a variable referencing a [SurfaceDeleteFaceFeatures](SurfaceDeleteFaceFeatures.md) object.

```python
returnValue = surfaceDeleteFaceFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SurfaceDeleteFaceFeature](SurfaceDeleteFaceFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2016  

