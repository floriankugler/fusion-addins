# TrimFeature.createForAssemblyContext Method

Parent Object: [TrimFeature](TrimFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"trimFeature_var" is a variable referencing a [TrimFeature](TrimFeature.md) object.

```python
returnValue = trimFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [TrimFeature](TrimFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version July 2015  

