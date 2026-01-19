# ChamferFeature.createForAssemblyContext Method

Parent Object: [ChamferFeature](ChamferFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"chamferFeature_var" is a variable referencing a [ChamferFeature](ChamferFeature.md) object.

```python
returnValue = chamferFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [ChamferFeature](ChamferFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version November 2014  

