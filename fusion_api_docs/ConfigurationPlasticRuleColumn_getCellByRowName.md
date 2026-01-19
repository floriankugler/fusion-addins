# ConfigurationPlasticRuleColumn.getCellByRowName Method

Parent Object: [ConfigurationPlasticRuleColumn](ConfigurationPlasticRuleColumn.md)  

## Description

Gets the cell in this column at the row specified by its name.

## Syntax

"configurationPlasticRuleColumn_var" is a variable referencing a [ConfigurationPlasticRuleColumn](ConfigurationPlasticRuleColumn.md) object.

```python
returnValue = configurationPlasticRuleColumn_var.getCellByRowName(rowName)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationPlasticRuleCell](ConfigurationPlasticRuleCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name    | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| rowName | string | The name of the row to return the cell for. |

## Version

Introduced in version January 2024  

