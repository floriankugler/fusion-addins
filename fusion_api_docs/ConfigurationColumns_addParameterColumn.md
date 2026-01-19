# ConfigurationColumns.addParameterColumn Method

Parent Object: [ConfigurationColumns](ConfigurationColumns.md)  

## Description

Adds a new parameter column to the configuration table. If a parameter column already exists for the parameter, the existing column is returned.  

This is only valid for TopConfigurationTable and ThemeConfigurationTable objects. It will fail for all other table types.

## Syntax

"configurationColumns_var" is a variable referencing a [ConfigurationColumns](ConfigurationColumns.md) object.

```python
returnValue = configurationColumns_var.addParameterColumn(parameter)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationParameterColumn](ConfigurationParameterColumn.md) | Returns the new column or null in the case of failure. |

## Parameters

| Name      | Type                       | Description                        |
|-----------|----------------------------|------------------------------------|
| parameter | [Parameter](Parameter.md) | The parameter to add to the table. |

## Version

Introduced in version March 2024  

