# BRepEdge.tangentiallyConnectedEdges Property

Parent Object: [BRepEdge](BRepEdge.md)  

## Description

Returns a collection of edges that includes all of the edges tangentially connected to this edge. The result includes this edge. The edges are in the collection in their connected order.

## Syntax

"bRepEdge_var" is a variable referencing a BRepEdge object.  

```python
# Get the value of the property.
propertyValue = bRepEdge_var.tangentiallyConnectedEdges
```

## Property Value

This is a read only property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version August 2014  

