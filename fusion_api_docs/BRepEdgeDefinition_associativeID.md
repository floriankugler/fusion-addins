# BRepEdgeDefinition.associativeID Property

Parent Object: [BRepEdgeDefinition](BRepEdgeDefinition.md)  

## Description

Gets and sets the associate ID of this edge definition. This ID will be copied to the corresponding edge when the BRepBodyDefinition is used to create a BrepBody. It is used internally by Fusion as the identifier for the edge and is used for tracking this geometry for parametric recomputes.

## Syntax

"bRepEdgeDefinition_var" is a variable referencing a BRepEdgeDefinition object.  

```python
# Get the value of the property.
propertyValue = bRepEdgeDefinition_var.associativeID

# Set the value of the property.
bRepEdgeDefinition_var.associativeID = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version September 2020  

