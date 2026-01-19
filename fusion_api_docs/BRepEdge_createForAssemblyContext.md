# BRepEdge.createForAssemblyContext Method

Parent Object: [BRepEdge](BRepEdge.md)  

## Description

Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"bRepEdge_var" is a variable referencing a [BRepEdge](BRepEdge.md) object.

```python
returnValue = bRepEdge_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [BRepEdge](BRepEdge.md) | Returns the new BrepEdge proxy or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context for the created proxy. |

## Version

Introduced in version August 2014  

