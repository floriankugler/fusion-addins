# ConfigurationColumns.item Method

Parent Object: [ConfigurationColumns](ConfigurationColumns.md)  

## Description

A method that returns the specified column object using an index into the collection.

## Syntax

"configurationColumns_var" is a variable referencing a [ConfigurationColumns](ConfigurationColumns.md) object.

```python
returnValue = configurationColumns_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationColumn](ConfigurationColumn.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version January 2024  

