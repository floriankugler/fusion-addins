# BRepEdge.pointOnEdge Property

Parent Object: [BRepEdge](BRepEdge.md)  

## Description

Returns a sample point guaranteed to lie on the edge's curve, within its boundaries, and not on a vertex (unless this is a degenerate edge).

## Syntax

"bRepEdge_var" is a variable referencing a BRepEdge object.  

```python
# Get the value of the property.
propertyValue = bRepEdge_var.pointOnEdge
```

## Property Value

This is a read only property whose value is a [Point3D](Point3D.md).

## Version

Introduced in version August 2014  

