# ConfigurationColumns.addInsertStandardDesignColumn Method

Parent Object: [ConfigurationColumns](ConfigurationColumns.md)  

## Description

Add a new column to control which standard design is used for an inserted design. If an insert column already exists for the occurrence, the existing column is returned.  

This is only valid for ConfigurationTopTable and ConfigurationCustomThemeTable objects and will fail for all other table types.

## Syntax

"configurationColumns_var" is a variable referencing a [ConfigurationColumns](ConfigurationColumns.md) object.

```python
returnValue = configurationColumns_var.addInsertStandardDesignColumn(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationInsertStandardDesignColumn](ConfigurationInsertStandardDesignColumn.md) | Returns the new column or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that references a standard design. |

## Version

Introduced in version September 2025  

