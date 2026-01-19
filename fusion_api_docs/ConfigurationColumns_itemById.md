# ConfigurationColumns.itemById Method

Parent Object: [ConfigurationColumns](ConfigurationColumns.md)  

## Description

A method that returns the specified column object using the ID of the column.

## Syntax

"configurationColumns_var" is a variable referencing a [ConfigurationColumns](ConfigurationColumns.md) object.

```python
returnValue = configurationColumns_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationColumn](ConfigurationColumn.md) | Returns the specified item or null if no column matches the provided ID. |

## Parameters

| Name | Type   | Description                                           |
|------|--------|-------------------------------------------------------|
| id   | string | The ID of the column within the collection to return. |

## Version

Introduced in version January 2024  

