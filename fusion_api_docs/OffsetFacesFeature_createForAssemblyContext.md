# OffsetFacesFeature.createForAssemblyContext Method

Parent Object: [OffsetFacesFeature](OffsetFacesFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"offsetFacesFeature_var" is a variable referencing an [OffsetFacesFeature](OffsetFacesFeature.md) object.

```python
returnValue = offsetFacesFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetFacesFeature](OffsetFacesFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version November 2025  

