# ConfigurationPlasticRuleColumn.deleteMe Method

Parent Object: [ConfigurationPlasticRuleColumn](ConfigurationPlasticRuleColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationPlasticRuleColumn_var" is a variable referencing a [ConfigurationPlasticRuleColumn](ConfigurationPlasticRuleColumn.md) object.

```python
returnValue = configurationPlasticRuleColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version March 2024  

