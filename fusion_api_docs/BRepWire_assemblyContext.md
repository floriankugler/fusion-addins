# BRepWire.assemblyContext Property

Parent Object: [BRepWire](BRepWire.md)  

## Description

Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this BRepFace object is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly. but is already the native object.

## Syntax

"bRepWire_var" is a variable referencing a BRepWire object.  

```python
# Get the value of the property.
propertyValue = bRepWire_var.assemblyContext
```

## Property Value

This is a read only property whose value is an [Occurrence](Occurrence.md).

## Samples

| Name | Description |
|----|----|
| [BrepWire Sample](BrepWireSample_Sample.md) | BrepWires and BrepWire related functions |

## Version

Introduced in version December 2017  

