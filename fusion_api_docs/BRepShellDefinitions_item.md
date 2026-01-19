# BRepShellDefinitions.item Method

Parent Object: [BRepShellDefinitions](BRepShellDefinitions.md)  

## Description

Function that returns the specified BRepShellDefinition object using an index into the collection.

## Syntax

"bRepShellDefinitions_var" is a variable referencing a [BRepShellDefinitions](BRepShellDefinitions.md) object.

```python
returnValue = bRepShellDefinitions_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BRepShellDefinition](BRepShellDefinition.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2020  

