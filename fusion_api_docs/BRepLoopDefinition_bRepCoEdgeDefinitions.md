# BRepLoopDefinition.bRepCoEdgeDefinitions Property

Parent Object: [BRepLoopDefinition](BRepLoopDefinition.md)  

## Description

Provides access to the BRepCoEdgeDefinitions object associated with the parent BRepFaceDefinition object. It's through the returned collection that you can create new BRepCoEdgeDefinition objects.

## Syntax

"bRepLoopDefinition_var" is a variable referencing a BRepLoopDefinition object.  

```python
# Get the value of the property.
propertyValue = bRepLoopDefinition_var.bRepCoEdgeDefinitions
```

## Property Value

This is a read only property whose value is a [BRepCoEdgeDefinitions](BRepCoEdgeDefinitions.md).

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

