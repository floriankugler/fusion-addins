# DeriveFeature.createForAssemblyContext Method

Parent Object: [DeriveFeature](DeriveFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"deriveFeature_var" is a variable referencing a [DeriveFeature](DeriveFeature.md) object.

```python
returnValue = deriveFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [DeriveFeature](DeriveFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version January 2026  

