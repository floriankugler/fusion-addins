# ConfigurationPlasticRuleColumns.add Method

Parent Object: [ConfigurationPlasticRuleColumns](ConfigurationPlasticRuleColumns.md)  

## Description

Adds a new column to the plastic rule table.

## Syntax

"configurationPlasticRuleColumns_var" is a variable referencing a [ConfigurationPlasticRuleColumns](ConfigurationPlasticRuleColumns.md) object.

```python
returnValue = configurationPlasticRuleColumns_var.add(component)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationPlasticRuleColumn](ConfigurationPlasticRuleColumn.md) | Returns the newly created ConfigurationPlasticRuleColumn object or null if it fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| component | [Component](Component.md) | The component whose active plastic rule will be controlled by this column. |

## Version

Introduced in version March 2024  

