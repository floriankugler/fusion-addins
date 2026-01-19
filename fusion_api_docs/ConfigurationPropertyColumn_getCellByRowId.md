# ConfigurationPropertyColumn.getCellByRowId Method

Parent Object: [ConfigurationPropertyColumn](ConfigurationPropertyColumn.md)  

## Description

Gets the cell in this column at the row specified by its ID.

## Syntax

"configurationPropertyColumn_var" is a variable referencing a [ConfigurationPropertyColumn](ConfigurationPropertyColumn.md) object.

```python
returnValue = configurationPropertyColumn_var.getCellByRowId(rowId)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationPropertyCell](ConfigurationPropertyCell.md) | Returns the specified cell if successful and null if the id is not found. |

## Parameters

| Name  | Type   | Description                               |
|-------|--------|-------------------------------------------|
| rowId | string | The ID of the row to return the cell for. |

## Version

Introduced in version January 2024  

