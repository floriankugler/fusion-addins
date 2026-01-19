# BRepFace.tangentiallyConnectedFaces Property

Parent Object: [BRepFace](BRepFace.md)  

## Description

Returns the set of faces that are tangentially adjacent to this face. In other words, it is the set of faces that are adjacent to this face's edges and have a smooth transition across those edges.

## Syntax

"bRepFace_var" is a variable referencing a BRepFace object.  

```python
# Get the value of the property.
propertyValue = bRepFace_var.tangentiallyConnectedFaces
```

## Property Value

This is a read only property whose value is a [BRepFaces](BRepFaces.md).

## Version

Introduced in version August 2014  

