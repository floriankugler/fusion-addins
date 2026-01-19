# ConfigurationThemeColumn.getCellByRowId Method

Parent Object: [ConfigurationThemeColumn](ConfigurationThemeColumn.md)  

## Description

Gets the cell in this column at the row specified by its ID.

## Syntax

"configurationThemeColumn_var" is a variable referencing a [ConfigurationThemeColumn](ConfigurationThemeColumn.md) object.

```python
returnValue = configurationThemeColumn_var.getCellByRowId(rowId)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationThemeCell](ConfigurationThemeCell.md) | Returns the specified cell if successful and null if the id is not found. |

## Parameters

| Name  | Type   | Description                               |
|-------|--------|-------------------------------------------|
| rowId | string | The ID of the row to return the cell for. |

## Version

Introduced in version January 2024  

