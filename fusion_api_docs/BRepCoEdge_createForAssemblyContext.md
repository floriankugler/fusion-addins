# BRepCoEdge.createForAssemblyContext Method

Parent Object: [BRepCoEdge](BRepCoEdge.md)  

## Description

Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"bRepCoEdge_var" is a variable referencing a [BRepCoEdge](BRepCoEdge.md) object.

```python
returnValue = bRepCoEdge_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [BRepCoEdge](BRepCoEdge.md) | Returns the new BrepCoEdge proxy or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context for the created proxy. |

## Version

Introduced in version August 2014  

