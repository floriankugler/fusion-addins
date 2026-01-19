# CommandInputs.itemById Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Returns the command input that has the specified ID.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [CommandInput](CommandInput.md) | Returns the specified command input or null if the input ID doesn't match an existing command input. |

## Parameters

| Name | Type   | Description                                         |
|------|--------|-----------------------------------------------------|
| id   | string | The unique ID of the command input you want to get. |

## Version

Introduced in version August 2014  

