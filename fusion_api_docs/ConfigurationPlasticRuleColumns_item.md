# ConfigurationPlasticRuleColumns.item Method

Parent Object: [ConfigurationPlasticRuleColumns](ConfigurationPlasticRuleColumns.md)  

## Description

A method that returns the specified column using an index into the collection. These are returned in the same order as they appear in the table.

## Syntax

"configurationPlasticRuleColumns_var" is a variable referencing a [ConfigurationPlasticRuleColumns](ConfigurationPlasticRuleColumns.md) object.

```python
returnValue = configurationPlasticRuleColumns_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationPlasticRuleColumn](ConfigurationPlasticRuleColumn.md) | Returns the specified column or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the column to return, where the first column is index 0. The name column is not included. |

## Version

Introduced in version January 2024  

