# ConfigurationRows.itemByName Method

Parent Object: [ConfigurationRows](ConfigurationRows.md)  

## Description

A method that returns the row with the specified name.

## Syntax

"configurationRows_var" is a variable referencing a [ConfigurationRows](ConfigurationRows.md) object.

```python
returnValue = configurationRows_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationRow](ConfigurationRow.md) | Returns the specified row or null if the named row does not exist. |

## Parameters

| Name | Type   | Description                    |
|------|--------|--------------------------------|
| name | string | The name of the row to return. |

## Version

Introduced in version January 2024  

