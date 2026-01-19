# ConfigurationAppearanceColumns.item Method

Parent Object: [ConfigurationAppearanceColumns](ConfigurationAppearanceColumns.md)  

## Description

A method that returns the specified column using an index into the collection. These are returned in the same order as they appear in the table.

## Syntax

"configurationAppearanceColumns_var" is a variable referencing a [ConfigurationAppearanceColumns](ConfigurationAppearanceColumns.md) object.

```python
returnValue = configurationAppearanceColumns_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationAppearanceColumn](ConfigurationAppearanceColumn.md) | Returns the specified column or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the column to return, where the first column is index 0. The name column is not included. |

## Version

Introduced in version January 2024  

