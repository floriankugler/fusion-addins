# PatchFeature.createForAssemblyContext Method

Parent Object: [PatchFeature](PatchFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e., a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"patchFeature_var" is a variable referencing a [PatchFeature](PatchFeature.md) object.

```python
returnValue = patchFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [PatchFeature](PatchFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy. |

## Version

Introduced in version July 2016  

