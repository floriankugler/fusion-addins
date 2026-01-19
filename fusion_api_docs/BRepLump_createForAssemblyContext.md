# BRepLump.createForAssemblyContext Method

Parent Object: [BRepLump](BRepLump.md)  

## Description

Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"bRepLump_var" is a variable referencing a [BRepLump](BRepLump.md) object.

```python
returnValue = bRepLump_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [BRepLump](BRepLump.md) | Returns the new BrepLump proxy or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context for the created proxy. |

## Version

Introduced in version August 2014  

