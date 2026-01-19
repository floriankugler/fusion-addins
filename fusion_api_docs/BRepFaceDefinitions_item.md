# BRepFaceDefinitions.item Method

Parent Object: [BRepFaceDefinitions](BRepFaceDefinitions.md)  

## Description

Function that returns the specified BRepFaceDefinition object using an index into the collection.

## Syntax

"bRepFaceDefinitions_var" is a variable referencing a [BRepFaceDefinitions](BRepFaceDefinitions.md) object.

```python
returnValue = bRepFaceDefinitions_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BRepFaceDefinition](BRepFaceDefinition.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2020  

