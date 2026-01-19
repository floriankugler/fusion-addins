# ConfigurationSheetMetalRuleColumns.add Method

Parent Object: [ConfigurationSheetMetalRuleColumns](ConfigurationSheetMetalRuleColumns.md)  

## Description

Adds a new column to the sheet metal rule table.

## Syntax

"configurationSheetMetalRuleColumns_var" is a variable referencing a [ConfigurationSheetMetalRuleColumns](ConfigurationSheetMetalRuleColumns.md) object.

```python
returnValue = configurationSheetMetalRuleColumns_var.add(component)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationSheetMetalRuleColumn](ConfigurationSheetMetalRuleColumn.md) | Returns the newly created ConfigurationPlasticRuleColumn object or null if it fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| component | [Component](Component.md) | The component whose active sheet metal rule will be controlled by this column. |

## Version

Introduced in version March 2024  

