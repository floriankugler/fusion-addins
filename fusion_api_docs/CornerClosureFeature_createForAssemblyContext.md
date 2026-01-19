# CornerClosureFeature.createForAssemblyContext Method

Parent Object: [CornerClosureFeature](CornerClosureFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"cornerClosureFeature_var" is a variable referencing a [CornerClosureFeature](CornerClosureFeature.md) object.

```python
returnValue = cornerClosureFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [CornerClosureFeature](CornerClosureFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version January 2026  

