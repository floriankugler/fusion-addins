# ConfigurationCustomThemeTables.item Method

Parent Object: [ConfigurationCustomThemeTables](ConfigurationCustomThemeTables.md)  

## Description

A method that returns the specified custom theme table using an index into the collection.

## Syntax

"configurationCustomThemeTables_var" is a variable referencing a [ConfigurationCustomThemeTables](ConfigurationCustomThemeTables.md) object.

```python
returnValue = configurationCustomThemeTables_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationCustomThemeTable](ConfigurationCustomThemeTable.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version January 2024  

