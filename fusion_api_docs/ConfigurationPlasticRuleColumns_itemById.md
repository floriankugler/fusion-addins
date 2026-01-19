# ConfigurationPlasticRuleColumns.itemById Method

Parent Object: [ConfigurationPlasticRuleColumns](ConfigurationPlasticRuleColumns.md)  

## Description

A method that returns the column with the specified ID.

## Syntax

"configurationPlasticRuleColumns_var" is a variable referencing a [ConfigurationPlasticRuleColumns](ConfigurationPlasticRuleColumns.md) object.

```python
returnValue = configurationPlasticRuleColumns_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationPlasticRuleColumn](ConfigurationPlasticRuleColumn.md) | Returns the specified column or null if a column with the specified ID does not exist. |

## Parameters

| Name | Type   | Description                     |
|------|--------|---------------------------------|
| id   | string | The id of the column to return. |

## Version

Introduced in version January 2024  

