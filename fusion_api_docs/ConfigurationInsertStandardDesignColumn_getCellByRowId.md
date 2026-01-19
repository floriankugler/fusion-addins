# ConfigurationInsertStandardDesignColumn.getCellByRowId Method

Parent Object: [ConfigurationInsertStandardDesignColumn](ConfigurationInsertStandardDesignColumn.md)  

## Description

Gets the cell in this column at the row specified by its ID.

## Syntax

"configurationInsertStandardDesignColumn_var" is a variable referencing a [ConfigurationInsertStandardDesignColumn](ConfigurationInsertStandardDesignColumn.md) object.

```python
returnValue = configurationInsertStandardDesignColumn_var.getCellByRowId(rowId)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationInsertStandardDesignCell](ConfigurationInsertStandardDesignCell.md) | Returns the specified cell if successful and null if the id is not found. |

## Parameters

| Name  | Type   | Description                               |
|-------|--------|-------------------------------------------|
| rowId | string | The ID of the row to return the cell for. |

## Version

Introduced in version September 2025  

