# ConfigurationParameterColumn.getCellByRowId Method

Parent Object: [ConfigurationParameterColumn](ConfigurationParameterColumn.md)  

## Description

Gets the cell in this column at the row specified by its ID.

## Syntax

"configurationParameterColumn_var" is a variable referencing a [ConfigurationParameterColumn](ConfigurationParameterColumn.md) object.

```python
returnValue = configurationParameterColumn_var.getCellByRowId(rowId)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationParameterCell](ConfigurationParameterCell.md) | Returns the specified cell if successful and null if the id is not found. |

## Parameters

| Name  | Type   | Description                               |
|-------|--------|-------------------------------------------|
| rowId | string | The ID of the row to return the cell for. |

## Version

Introduced in version January 2024  

