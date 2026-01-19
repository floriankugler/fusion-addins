# ConfigurationRow.getCellByColumnId Method

Parent Object: [ConfigurationRow](ConfigurationRow.md)  

## Description

Gets the cell in this row at the column with the specified ID.

## Syntax

"configurationRow_var" is a variable referencing a [ConfigurationRow](ConfigurationRow.md) object.

```python
returnValue = configurationRow_var.getCellByColumnId(columnId)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationCell](ConfigurationCell.md) | Returns the specified cell if successful or null if a column with the specified ID does not exist. |

## Parameters

| Name     | Type   | Description                          |
|----------|--------|--------------------------------------|
| columnId | string | The ID of the column the cell is in. |

## Version

Introduced in version January 2024  

