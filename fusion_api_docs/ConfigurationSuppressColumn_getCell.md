# ConfigurationSuppressColumn.getCell Method

Parent Object: [ConfigurationSuppressColumn](ConfigurationSuppressColumn.md)  

## Description

Gets the cell in this column at the specified row. The first row has an index of 0 and does not include the header row.

## Syntax

"configurationSuppressColumn_var" is a variable referencing a [ConfigurationSuppressColumn](ConfigurationSuppressColumn.md) object.

```python
returnValue = configurationSuppressColumn_var.getCell(rowIndex)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationSuppressCell](ConfigurationSuppressCell.md) | Returns the specified cell if successful and null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| rowIndex | uinteger | The index of the row to return the cell for. The first row has an index of 0. |

## Version

Introduced in version January 2024  

