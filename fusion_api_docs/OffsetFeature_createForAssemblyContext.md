# OffsetFeature.createForAssemblyContext Method

Parent Object: [OffsetFeature](OffsetFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"offsetFeature_var" is a variable referencing an [OffsetFeature](OffsetFeature.md) object.

```python
returnValue = offsetFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetFeature](OffsetFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version June 2015  

