# CommandDefinitions.item Method

Parent Object: [CommandDefinitions](CommandDefinitions.md)  

## Description

Returns the CommandDefinition at the specified index.

## Syntax

"commandDefinitions_var" is a variable referencing a [CommandDefinitions](CommandDefinitions.md) object.

```python
returnValue = commandDefinitions_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CommandDefinition](CommandDefinition.md) | Returns the CommandDefinition at the specified index or null if an invalid index is specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the command definition within the collection to return. The first item in the collection has in index of 0. |

## Version

Introduced in version August 2014  

