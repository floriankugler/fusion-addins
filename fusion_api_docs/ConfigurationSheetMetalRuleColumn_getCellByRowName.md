# ConfigurationSheetMetalRuleColumn.getCellByRowName Method

Parent Object: [ConfigurationSheetMetalRuleColumn](ConfigurationSheetMetalRuleColumn.md)  

## Description

Gets the cell in this column at the row specified by its name.

## Syntax

"configurationSheetMetalRuleColumn_var" is a variable referencing a [ConfigurationSheetMetalRuleColumn](ConfigurationSheetMetalRuleColumn.md) object.

```python
returnValue = configurationSheetMetalRuleColumn_var.getCellByRowName(rowName)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationSheetMetalRuleCell](ConfigurationSheetMetalRuleCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name    | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| rowName | string | The name of the row to return the cell for. |

## Version

Introduced in version January 2024  

