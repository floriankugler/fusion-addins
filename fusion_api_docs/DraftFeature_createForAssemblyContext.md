# DraftFeature.createForAssemblyContext Method

Parent Object: [DraftFeature](DraftFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"draftFeature_var" is a variable referencing a [DraftFeature](DraftFeature.md) object.

```python
returnValue = draftFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [DraftFeature](DraftFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version January 2015  

