# ConfigurationPropertyColumn.getCell Method

Parent Object: [ConfigurationPropertyColumn](ConfigurationPropertyColumn.md)  

## Description

Gets the cell in this column at the specified row. The first row has an index of 0 and does not include the header row.

## Syntax

"configurationPropertyColumn_var" is a variable referencing a [ConfigurationPropertyColumn](ConfigurationPropertyColumn.md) object.

```python
returnValue = configurationPropertyColumn_var.getCell(rowIndex)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationPropertyCell](ConfigurationPropertyCell.md) | Returns the specified cell if successful and null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| rowIndex | uinteger | The index of the row to return the cell for. The first row has an index of 0. |

## Version

Introduced in version January 2024  

