# PipeFeature.createForAssemblyContext Method

Parent Object: [PipeFeature](PipeFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"pipeFeature_var" is a variable referencing a [PipeFeature](PipeFeature.md) object.

```python
returnValue = pipeFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [PipeFeature](PipeFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version October 2023  

