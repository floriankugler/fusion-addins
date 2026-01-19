# BRepWireEdgeDefinition.associativeID Property

Parent Object: [BRepWireEdgeDefinition](BRepWireEdgeDefinition.md)  

## Description

Gets and sets the associate ID of this B-Rep wire definition. This ID will be copied to the corresponding edge when the BRepBodyDefinition is used to create a BrepBody. It is used by Fusion as the identifier for the edge and is used for tracking this geometry for parametric recomputes.

## Syntax

"bRepWireEdgeDefinition_var" is a variable referencing a BRepWireEdgeDefinition object.  

```python
# Get the value of the property.
propertyValue = bRepWireEdgeDefinition_var.associativeID

# Set the value of the property.
bRepWireEdgeDefinition_var.associativeID = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

