# MirrorFeature.createForAssemblyContext Method

Parent Object: [MirrorFeature](MirrorFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"mirrorFeature_var" is a variable referencing a [MirrorFeature](MirrorFeature.md) object.

```python
returnValue = mirrorFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [MirrorFeature](MirrorFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version November 2014  

