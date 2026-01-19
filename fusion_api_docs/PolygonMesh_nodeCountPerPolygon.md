# PolygonMesh.nodeCountPerPolygon Property

Parent Object: [PolygonMesh](PolygonMesh.md)  

## Description

Returns the number of nodes that define each polygon. For example, if NodeCountPerPolygon\[0\] returns 6 it indicates the first polygon is defined using 6 nodes. The first six indices returned by the PolygonNodeIndices properties provide the look-up into the NodeCoordinates array.

## Syntax

"polygonMesh_var" is a variable referencing a PolygonMesh object.  

```python
# Get the value of the property.
propertyValue = polygonMesh_var.nodeCountPerPolygon
```

## Property Value

This is a read only property whose value is an array of type integer.

## Version

Introduced in version August 2014  

