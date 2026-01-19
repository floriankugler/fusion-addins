# BoundaryFillFeature.createForAssemblyContext Method

Parent Object: [BoundaryFillFeature](BoundaryFillFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"boundaryFillFeature_var" is a variable referencing a [BoundaryFillFeature](BoundaryFillFeature.md) object.

```python
returnValue = boundaryFillFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [BoundaryFillFeature](BoundaryFillFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version June 2015  

