# RuledSurfaceFeature.createForAssemblyContext Method

Parent Object: [RuledSurfaceFeature](RuledSurfaceFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"ruledSurfaceFeature_var" is a variable referencing a [RuledSurfaceFeature](RuledSurfaceFeature.md) object.

```python
returnValue = ruledSurfaceFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [RuledSurfaceFeature](RuledSurfaceFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version September 2020  

