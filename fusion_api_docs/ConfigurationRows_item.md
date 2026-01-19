# ConfigurationRows.item Method

Parent Object: [ConfigurationRows](ConfigurationRows.md)  

## Description

A method that returns the specified row using an index into the collection. These are returned in the same order as in the table; the first row is the default row.

## Syntax

"configurationRows_var" is a variable referencing a [ConfigurationRows](ConfigurationRows.md) object.

```python
returnValue = configurationRows_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationRow](ConfigurationRow.md) | Returns the specified row or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the row to return, where the first row is index 0. The headers do not count as a row. |

## Version

Introduced in version January 2024  

