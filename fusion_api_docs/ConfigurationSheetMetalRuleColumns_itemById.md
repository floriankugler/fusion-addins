# ConfigurationSheetMetalRuleColumns.itemById Method

Parent Object: [ConfigurationSheetMetalRuleColumns](ConfigurationSheetMetalRuleColumns.md)  

## Description

A method that returns the column with the specified ID.

## Syntax

"configurationSheetMetalRuleColumns_var" is a variable referencing a [ConfigurationSheetMetalRuleColumns](ConfigurationSheetMetalRuleColumns.md) object.

```python
returnValue = configurationSheetMetalRuleColumns_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationSheetMetalRuleColumn](ConfigurationSheetMetalRuleColumn.md) | Returns the specified column or null if a column with the specified ID does not exist. |

## Parameters

| Name | Type   | Description                     |
|------|--------|---------------------------------|
| id   | string | The id of the column to return. |

## Version

Introduced in version January 2024  

