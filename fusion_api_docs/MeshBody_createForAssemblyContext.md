# MeshBody.createForAssemblyContext Method

Parent Object: [MeshBody](MeshBody.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. Fails if this object is not the NativeObject.

## Syntax

"meshBody_var" is a variable referencing a [MeshBody](MeshBody.md) object.

```python
returnValue = meshBody_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [MeshBody](MeshBody.md) | Returns the proxy for the occurrence in the context of the specified occurrence. Returns null if it failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that represents the context you want to create this proxy in. |

## Version

Introduced in version August 2014  

