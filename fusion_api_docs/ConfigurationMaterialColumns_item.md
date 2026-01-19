# ConfigurationMaterialColumns.item Method

Parent Object: [ConfigurationMaterialColumns](ConfigurationMaterialColumns.md)  

## Description

A method that returns the specified column using an index into the collection. These are returned in the same order as they appear in the table.

## Syntax

"configurationMaterialColumns_var" is a variable referencing a [ConfigurationMaterialColumns](ConfigurationMaterialColumns.md) object.

```python
returnValue = configurationMaterialColumns_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationMaterialColumn](ConfigurationMaterialColumn.md) | Returns the specified column or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the column to return, where the first column is index 0. The name column is not included. |

## Version

Introduced in version January 2024  

