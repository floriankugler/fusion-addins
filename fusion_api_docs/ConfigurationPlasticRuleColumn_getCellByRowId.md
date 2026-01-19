# ConfigurationPlasticRuleColumn.getCellByRowId Method

Parent Object: [ConfigurationPlasticRuleColumn](ConfigurationPlasticRuleColumn.md)  

## Description

Gets the cell in this column at the row specified by its ID.

## Syntax

"configurationPlasticRuleColumn_var" is a variable referencing a [ConfigurationPlasticRuleColumn](ConfigurationPlasticRuleColumn.md) object.

```python
returnValue = configurationPlasticRuleColumn_var.getCellByRowId(rowId)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationPlasticRuleCell](ConfigurationPlasticRuleCell.md) | Returns the specified cell if successful and null if the id is not found. |

## Parameters

| Name  | Type   | Description                               |
|-------|--------|-------------------------------------------|
| rowId | string | The ID of the row to return the cell for. |

## Version

Introduced in version January 2024  

