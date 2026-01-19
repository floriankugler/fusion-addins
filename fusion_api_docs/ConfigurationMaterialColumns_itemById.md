# ConfigurationMaterialColumns.itemById Method

Parent Object: [ConfigurationMaterialColumns](ConfigurationMaterialColumns.md)  

## Description

A method that returns the column with the specified ID.

## Syntax

"configurationMaterialColumns_var" is a variable referencing a [ConfigurationMaterialColumns](ConfigurationMaterialColumns.md) object.

```python
returnValue = configurationMaterialColumns_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationMaterialColumn](ConfigurationMaterialColumn.md) | Returns the specified column or null if a column with the specified ID does not exist. |

## Parameters

| Name | Type   | Description                     |
|------|--------|---------------------------------|
| id   | string | The id of the column to return. |

## Version

Introduced in version January 2024  

