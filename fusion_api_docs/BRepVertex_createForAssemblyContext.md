# BRepVertex.createForAssemblyContext Method

Parent Object: [BRepVertex](BRepVertex.md)  

## Description

Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"bRepVertex_var" is a variable referencing a [BRepVertex](BRepVertex.md) object.

```python
returnValue = bRepVertex_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [BRepVertex](BRepVertex.md) | Returns the new BrepVertex proxy or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context for the created proxy. |

## Version

Introduced in version August 2014  

