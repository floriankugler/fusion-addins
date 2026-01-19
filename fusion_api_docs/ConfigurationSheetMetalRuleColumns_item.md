# ConfigurationSheetMetalRuleColumns.item Method

Parent Object: [ConfigurationSheetMetalRuleColumns](ConfigurationSheetMetalRuleColumns.md)  

## Description

A method that returns the specified column using an index into the collection. These are returned in the same order as they appear in the table.

## Syntax

"configurationSheetMetalRuleColumns_var" is a variable referencing a [ConfigurationSheetMetalRuleColumns](ConfigurationSheetMetalRuleColumns.md) object.

```python
returnValue = configurationSheetMetalRuleColumns_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationSheetMetalRuleColumn](ConfigurationSheetMetalRuleColumn.md) | Returns the specified column or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the column to return, where the first column is index 0. The name column is not included. |

## Version

Introduced in version January 2024  

