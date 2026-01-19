# ConfigurationSuppressColumn.getCellByRowId Method

Parent Object: [ConfigurationSuppressColumn](ConfigurationSuppressColumn.md)  

## Description

Gets the cell in this column at the row specified by its ID.

## Syntax

"configurationSuppressColumn_var" is a variable referencing a [ConfigurationSuppressColumn](ConfigurationSuppressColumn.md) object.

```python
returnValue = configurationSuppressColumn_var.getCellByRowId(rowId)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationSuppressCell](ConfigurationSuppressCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name  | Type   | Description                               |
|-------|--------|-------------------------------------------|
| rowId | string | The ID of the row to return the cell for. |

## Version

Introduced in version January 2024  

