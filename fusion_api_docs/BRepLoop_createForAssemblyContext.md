# BRepLoop.createForAssemblyContext Method

Parent Object: [BRepLoop](BRepLoop.md)  

## Description

Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"bRepLoop_var" is a variable referencing a [BRepLoop](BRepLoop.md) object.

```python
returnValue = bRepLoop_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [BRepLoop](BRepLoop.md) | Returns the new BrepLoop proxy or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context for the created proxy. |

## Version

Introduced in version August 2014  

