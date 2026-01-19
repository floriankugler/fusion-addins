# SurfaceDeleteFaceFeatures.add Method

Parent Object: [SurfaceDeleteFaceFeatures](SurfaceDeleteFaceFeatures.md)  

## Description

Creates a new SurfaceDeleteFaceFeature feature. This deletes the specified faces from their bodies without any attempt to heal the openings. This is equivalent to selecting and deleting faces when in the Patch workspace.

## Syntax

"surfaceDeleteFaceFeatures_var" is a variable referencing a [SurfaceDeleteFaceFeatures](SurfaceDeleteFaceFeatures.md) object.

```python
returnValue = surfaceDeleteFaceFeatures_var.add(facesToDelete)
```

## Return Value

| Type | Description |
|----|----|
| [SurfaceDeleteFaceFeature](SurfaceDeleteFaceFeature.md) | Returns the newly created SurfaceDeleteFaceFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| facesToDelete | [Base](Base.md) | A single BRepFace or an ObjectCollection containing multiple BRepFace objects. |

## Samples

| Name | Description |
|----|----|
| [DeleteFace Feature API Sample](DeleteFaceFeatureSample_Sample.md) | Demonstrates creating a new deleteFace feature. |
| [surfaceDeleteFeatures.add](surfaceDeleteFeatures_add_Sample.md) | Demonstrates the surfaceDeleteFeatures.add method. |

## Version

Introduced in version August 2016  

