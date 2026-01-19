# ConfigurationVisibilityColumn.getCell Method

Parent Object: [ConfigurationVisibilityColumn](ConfigurationVisibilityColumn.md)  

## Description

Gets the cell in this column at the specified row. The first row has an index of 0 and does not include the header row.

## Syntax

"configurationVisibilityColumn_var" is a variable referencing a [ConfigurationVisibilityColumn](ConfigurationVisibilityColumn.md) object.

```python
returnValue = configurationVisibilityColumn_var.getCell(rowIndex)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationVisibilityCell](ConfigurationVisibilityCell.md) | Returns the specified cell if successful and null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| rowIndex | uinteger | The index of the row to return the cell for. The first row has an index of 0. |

## Version

Introduced in version January 2024  

