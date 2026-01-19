# BRepShell.createForAssemblyContext Method

Parent Object: [BRepShell](BRepShell.md)  

## Description

Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"bRepShell_var" is a variable referencing a [BRepShell](BRepShell.md) object.

```python
returnValue = bRepShell_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [BRepShell](BRepShell.md) | Returns the new BrepShell proxy or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context for the created proxy. |

## Version

Introduced in version August 2014  

