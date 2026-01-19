# DeleteFaceFeatures.add Method

Parent Object: [DeleteFaceFeatures](DeleteFaceFeatures.md)  

## Description

Creates a new SurfaceDeleteFace feature. This deletes the specified faces from their bodies and attempts to heal the body. The method will fail if the body cannot be healed. This is equivalent to selecting and deleting faces when in the Patch workspace.

## Syntax

"deleteFaceFeatures_var" is a variable referencing a [DeleteFaceFeatures](DeleteFaceFeatures.md) object.

```python
returnValue = deleteFaceFeatures_var.add(facesToDelete)
```

## Return Value

| Type | Description |
|----|----|
| [DeleteFaceFeature](DeleteFaceFeature.md) | Returns the newly created DeleteFaceFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| facesToDelete | [Base](Base.md) | A single BRepFace or an ObjectCollection containing multiple BRepFace objects. |

## Version

Introduced in version August 2016  

