# CommandInputs.item Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Returns the specified command input using an index into the collection.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CommandInput](CommandInput.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

