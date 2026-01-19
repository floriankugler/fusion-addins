# BRepWire.createForAssemblyContext Method

Parent Object: [BRepWire](BRepWire.md)  

## Description

Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"bRepWire_var" is a variable referencing a [BRepWire](BRepWire.md) object.

```python
returnValue = bRepWire_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [BRepWire](BRepWire.md) | Returns the new BRepWire proxy or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context for the created proxy. |

## Samples

| Name | Description |
|----|----|
| [BrepWire Sample](BrepWireSample_Sample.md) | BrepWires and BrepWire related functions |

## Version

Introduced in version December 2017  

