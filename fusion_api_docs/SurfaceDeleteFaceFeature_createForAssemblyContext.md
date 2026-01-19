# SurfaceDeleteFaceFeature.createForAssemblyContext Method

Parent Object: [SurfaceDeleteFaceFeature](SurfaceDeleteFaceFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"surfaceDeleteFaceFeature_var" is a variable referencing a [SurfaceDeleteFaceFeature](SurfaceDeleteFaceFeature.md) object.

```python
returnValue = surfaceDeleteFaceFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SurfaceDeleteFaceFeature](SurfaceDeleteFaceFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2016  

