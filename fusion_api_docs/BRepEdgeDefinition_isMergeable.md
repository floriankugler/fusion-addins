# BRepEdgeDefinition.isMergeable Property

Parent Object: [BRepEdgeDefinition](BRepEdgeDefinition.md)  

## Description

Gets and sets if the two faces that share this edge can be merged along this edge. This property defaults to true so that merging is always done but this can be set to false in cases where you want to preserve the edge.  

An example where merging is typically done is when you have multiple planar faces that all lie on the same plane and are connected. When merging is allowed these faces can be replaced by a single face and the edges connecting the faces (the merged edges) are no longer part of the body.

## Syntax

"bRepEdgeDefinition_var" is a variable referencing a BRepEdgeDefinition object.  

```python
# Get the value of the property.
propertyValue = bRepEdgeDefinition_var.isMergeable

# Set the value of the property.
bRepEdgeDefinition_var.isMergeable = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2020  

