# BRepLump.assemblyContext Property

Parent Object: [BRepLump](BRepLump.md)  

## Description

Returns the assembly context that is directly referencing this object in an assembly. This is only valid in the case where this BRepLump object is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly. but is already the native object.

## Syntax

"bRepLump_var" is a variable referencing a BRepLump object.  

```python
# Get the value of the property.
propertyValue = bRepLump_var.assemblyContext
```

## Property Value

This is a read only property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version August 2014  

