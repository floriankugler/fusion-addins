# ScaleFeature.createForAssemblyContext Method

Parent Object: [ScaleFeature](ScaleFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"scaleFeature_var" is a variable referencing a [ScaleFeature](ScaleFeature.md) object.

```python
returnValue = scaleFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [ScaleFeature](ScaleFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version January 2015  

