# ConfigurationAppearanceColumns.itemById Method

Parent Object: [ConfigurationAppearanceColumns](ConfigurationAppearanceColumns.md)  

## Description

A method that returns the column with the specified ID.

## Syntax

"configurationAppearanceColumns_var" is a variable referencing a [ConfigurationAppearanceColumns](ConfigurationAppearanceColumns.md) object.

```python
returnValue = configurationAppearanceColumns_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationAppearanceColumn](ConfigurationAppearanceColumn.md) | Returns the specified column or null if a column with the specified ID does not exist. |

## Parameters

| Name | Type   | Description                     |
|------|--------|---------------------------------|
| id   | string | The id of the column to return. |

## Version

Introduced in version January 2024  

