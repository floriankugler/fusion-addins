# BRepFace.createForAssemblyContext Method

Parent Object: [BRepFace](BRepFace.md)  

## Description

Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"bRepFace_var" is a variable referencing a [BRepFace](BRepFace.md) object.

```python
returnValue = bRepFace_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [BRepFace](BRepFace.md) | Returns the new BRepFace proxy or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context for the created proxy. |

## Version

Introduced in version August 2014  

