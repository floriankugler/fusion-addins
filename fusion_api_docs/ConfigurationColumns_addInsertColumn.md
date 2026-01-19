# ConfigurationColumns.addInsertColumn Method

Parent Object: [ConfigurationColumns](ConfigurationColumns.md)  

## Description

Add a new column to control which configuration is used for an inserted configuration. If an insert column already exists for the occurrence, the existing column is returned.  

This is only valid for ConfigurationTopTable and ConfigurationCustomThemeTable objects and will fail for all other table types.

## Syntax

"configurationColumns_var" is a variable referencing a [ConfigurationColumns](ConfigurationColumns.md) object.

```python
returnValue = configurationColumns_var.addInsertColumn(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationInsertColumn](ConfigurationInsertColumn.md) | Returns the new column or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that references a configuration. |

## Version

Introduced in version March 2024  

