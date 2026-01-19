# ConfigurationRows.itemById Method

Parent Object: [ConfigurationRows](ConfigurationRows.md)  

## Description

A method that returns the row with the specified ID.

## Syntax

"configurationRows_var" is a variable referencing a [ConfigurationRows](ConfigurationRows.md) object.

```python
returnValue = configurationRows_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationRow](ConfigurationRow.md) | Returns the specified row or null if a row with the specified ID does not exist. |

## Parameters

| Name | Type   | Description                  |
|------|--------|------------------------------|
| id   | string | The id of the row to return. |

## Version

Introduced in version January 2024  

