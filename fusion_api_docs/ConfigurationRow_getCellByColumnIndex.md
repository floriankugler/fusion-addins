# ConfigurationRow.getCellByColumnIndex Method

Parent Object: [ConfigurationRow](ConfigurationRow.md)  

## Description

Gets the cell in this row at the specified column index. The first column has an index of 0 and does not include the name column.

## Syntax

"configurationRow_var" is a variable referencing a [ConfigurationRow](ConfigurationRow.md) object.

```python
returnValue = configurationRow_var.getCellByColumnIndex(columnIndex)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationCell](ConfigurationCell.md) | Returns the specified cell if successful and null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| columnIndex | uinteger | The index of the column to return the cell for. The first column has an index 0. |

## Version

Introduced in version January 2024  

