# BRepBody.createForAssemblyContext Method

Parent Object: [BRepBody](BRepBody.md)  

## Description

Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.  

This method is only valid if the IsTransient property is false.

## Syntax

"bRepBody_var" is a variable referencing a [BRepBody](BRepBody.md) object.

```python
returnValue = bRepBody_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the new BRepBoy proxy or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context for the created proxy. |

## Version

Introduced in version August 2014  

