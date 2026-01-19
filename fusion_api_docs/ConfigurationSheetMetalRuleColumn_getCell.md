# ConfigurationSheetMetalRuleColumn.getCell Method

Parent Object: [ConfigurationSheetMetalRuleColumn](ConfigurationSheetMetalRuleColumn.md)  

## Description

Gets the cell in this column at the specified row. The first row has an index of 0 and does not include the header row.

## Syntax

"configurationSheetMetalRuleColumn_var" is a variable referencing a [ConfigurationSheetMetalRuleColumn](ConfigurationSheetMetalRuleColumn.md) object.

```python
returnValue = configurationSheetMetalRuleColumn_var.getCell(rowIndex)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationSheetMetalRuleCell](ConfigurationSheetMetalRuleCell.md) | Returns the specified cell if successful and null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| rowIndex | uinteger | The index of the row to return the cell for. The first row has an index of 0. |

## Version

Introduced in version January 2024  

